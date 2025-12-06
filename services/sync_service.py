import asyncio
from typing import List, Dict, Any
from core.config import settings

def split_name(fullname: str):
    parts = fullname.strip().split(" ", 1)
    firstname = parts[0] if parts[0] else "Nombre"
    lastname = parts[1] if len(parts) > 1 and parts[1].strip() else "Apellido"
    return firstname, lastname

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

        # ========= GRUPO ==========
        query = """
        SELECT g.id as grupo_id, g.nombre as grupo_nombre, g.asignatura_id, g.docente_id, g.cuatrimestre_id
        FROM grupo g WHERE g.id = :gid
        """
        group = await self.db.fetch_one(query=query, values={"gid": grupo_id})
        if not group:
            return {"error": "grupo_not_found", "grupo_id": grupo_id}

        asign = await self.db.fetch_one(
            "SELECT id,nombre FROM asignatura WHERE id = :id",
            values={"id": group["asignatura_id"]}
        )

        doc = await self.db.fetch_one(
            "SELECT id,nombre,correo FROM docente WHERE id = :id",
            values={"id": group["docente_id"]}
        )

        alumnos = await self.db.fetch_all(
            """
            SELECT a.id, a.nombre, a.matricula, a.correo
            FROM alumno a
            JOIN grupo_alumno ga ON ga.alumno_id = a.id
            WHERE ga.grupo_id = :gid
            """,
            values={"gid": grupo_id}
        )

        shortname = f"P1_C{group['cuatrimestre_id']}_A{asign['id']}_G{group['grupo_id']}"
        fullname = f"Grupo {group['grupo_nombre']} - {asign['nombre']}"

        summary = {"course": None, "teacher": None, "students": [], "errors": []}

        # ========= CURSO ==========
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

        # ========= DOCENTE ==========
        teacher_id = None
        if doc:
            async with sem:
                try:
                    firstname, lastname = split_name(doc["nombre"])
                    email = doc["correo"] if doc["correo"] else f"doc{doc['id']}@local"

                    uresp = await self.moodle.get_user_by_email(email)

                    if uresp.get("users"):
                        teacher_id = uresp["users"][0]["id"]
                    else:
                        username = f"doc{doc['id']}"

                        created = await self.moodle.create_user(
                            username=username,
                            firstname=firstname,
                            lastname=lastname,
                            email=email
                        )
                        teacher_id = created[0]["id"]

                    summary["teacher"] = {"id": teacher_id, "nombre": doc["nombre"]}

                except Exception as e:
                    summary["errors"].append({"stage": "teacher", "error": str(e)})

        # ========= ALUMNOS ==========
        async def handle_student(a):
            try:
                firstname, lastname = split_name(a["nombre"])
                email = a["correo"] if a["correo"] else f"{a['matricula'] or 'al'+str(a['id'])}@local"
                username = a["matricula"] or f"al{a['id']}"

                uresp = await self.moodle.get_user_by_email(email)

                if uresp.get("users"):
                    uid = uresp["users"][0]["id"]
                    existed = True
                else:
                    created = await self.moodle.create_user(
                        username=username,
                        firstname=firstname,
                        lastname=lastname,
                        email=email
                    )
                    uid = created[0]["id"]
                    existed = False

                await self.moodle.enrol_user(uid, courseid, roleid=5)

                return {"alumno_id": a["id"], "moodle_id": uid, "status": "ok", "existed": existed}

            except Exception as e:
                return {"alumno_id": a["id"], "status": "error", "error": str(e)}

        tasks = [handle_student(a) for a in alumnos]

        sem_local = asyncio.Semaphore(settings.concurrency_limit)

        async def limited(coro):
            async with sem_local:
                return await coro

        summary["students"] = await asyncio.gather(*(limited(t) for t in tasks))

        return summary
