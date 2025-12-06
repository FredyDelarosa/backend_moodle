import asyncio
from typing import List, Dict, Any
from core.config import settings

class SyncService:
    def __init__(self, db, moodle_client):
        self.db = db
        self.moodle = moodle_client
        self.semaphore = asyncio.Semaphore(settings.concurrency_limit)

    async def sync_group(self, grupo_id: int, create_if_missing: bool = True, concurrency_limit: int | None = None) -> Dict[str, Any]:
        if concurrency_limit:
            sem = asyncio.Semaphore(concurrency_limit)
        else:
            sem = self.semaphore

        query = """
        SELECT g.id as grupo_id, g.nombre as grupo_nombre, g.asignatura_id, g.docente_id, g.cuatrimestre_id
        FROM grupo g WHERE g.id = :gid
        """
        group = await self.db.fetch_one(query=query, values={"gid": grupo_id})
        if not group:
            return {"error": "grupo_not_found", "grupo_id": grupo_id}

        asign_q = "SELECT id,nombre FROM asignatura WHERE id = :id"
        asign = await self.db.fetch_one(query=asign_q, values={"id": group["asignatura_id"]})
        doc_q = "SELECT id,nombre,correo FROM docente WHERE id = :id"
        doc = await self.db.fetch_one(query=doc_q, values={"id": group["docente_id"]})

        alum_q = """
        SELECT a.id, a.nombre, a.matricula, a.correo FROM alumno a
        JOIN grupo_alumno ga ON ga.alumno_id = a.id
        WHERE ga.grupo_id = :gid
        """
        alumnos = await self.db.fetch_all(query=alum_q, values={"gid": grupo_id})

        shortname = f"P1_C{group['cuatrimestre_id']}_A{asign['id']}_G{group['grupo_id']}"
        fullname = f"Grupo {group['grupo_nombre']} - {asign['nombre']}"

        summary = {"course": None, "teacher": None, "students": [], "errors": []}

        async with sem:
            try:
                resp = await self.moodle.get_course_by_shortname(shortname)
                if resp.get("courses"):
                    courseid = resp["courses"][0]["id"]
                else:
                    if create_if_missing:
                        created = await self.moodle.create_course(fullname, shortname)
                        courseid = created[0]["id"]
                    else:
                        courseid = None
                summary["course"] = {"shortname": shortname, "id": courseid}
            except Exception as e:
                summary["errors"].append({"stage": "course", "error": str(e)})
                return summary

        teacher_id = None
        if doc:
            async with sem:
                try:
                    if doc["correo"]:
                        uresp = await self.moodle.get_user_by_email(doc["correo"])
                        if uresp.get("users"):
                            teacher_id = uresp["users"][0]["id"]
                        else:
                            username = f"doc{doc['id']}"
                            parts = doc["nombre"].split(" ",1)
                            firstname = parts[0]
                            lastname = parts[1] if len(parts)>1 else ""
                            created = await self.moodle.create_user(username, firstname, lastname, doc["correo"])
                            teacher_id = created[0]["id"]
                    else:
                        username = f"doc{doc['id']}"
                        created = await self.moodle.create_user(username, doc["nombre"].split(" ")[0], " ", f"doc{doc['id']}@example.local")
                        teacher_id = created[0]["id"]
                    summary["teacher"] = {"id": teacher_id, "nombre": doc["nombre"]}
                except Exception as e:
                    summary["errors"].append({"stage": "teacher", "error": str(e)})

        async def handle_student(a):
            try:
                if a["correo"]:
                    uresp = await self.moodle.get_user_by_email(a["correo"])
                    if uresp.get("users"):
                        uid = uresp["users"][0]["id"]
                        existed = True
                    else:
                        username = a["matricula"] or f"al{a['id']}"
                        parts = a["nombre"].split(" ",1)
                        firstname = parts[0]
                        lastname = parts[1] if len(parts)>1 else ""
                        created = await self.moodle.create_user(username, firstname, lastname, a["correo"])
                        uid = created[0]["id"]
                        existed = False
                else:
                    username = a["matricula"] or f"al{a['id']}"
                    created = await self.moodle.create_user(username, a["nombre"].split(" ")[0], " ", f"{username}@example.local")
                    uid = created[0]["id"]
                    existed = False

                await self.moodle.enrol_user(uid, courseid, roleid=5)
                return {"alumno_id": a["id"], "moodle_id": uid, "status": "ok", "existed": existed}
            except Exception as e:
                return {"alumno_id": a["id"], "status": "error", "error": str(e)}

        tasks = []
        for a in alumnos:
            tasks.append(handle_student(a))

        sem_local = asyncio.Semaphore(settings.concurrency_limit)
        async def limited(coro):
            async with sem_local:
                return await coro

        results = await asyncio.gather(*(limited(t) for t in tasks))
        summary["students"] = results

        return summary
