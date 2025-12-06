from db.database import database

class AcademyService:
    def __init__(self, db=database):
        self.db = db

    async def create_programa(self, nombre: str, numero_cuatrimestres: int):
        query = """
        INSERT INTO programa_estudio (nombre, numero_cuatrimestres)
        VALUES (:nombre, :nc)
        """
        last_id = await self.db.execute(query, {"nombre": nombre, "nc": numero_cuatrimestres})
        return last_id

    async def list_programas(self):
        return await self.db.fetch_all("SELECT * FROM programa_estudio")

    async def get_programa(self, programa_id: int):
        return await self.db.fetch_one(
            "SELECT * FROM programa_estudio WHERE id = :id",
            {"id": programa_id}
        )

    async def update_programa(self, programa_id: int, data: dict):
        query = """
        UPDATE programa_estudio
        SET nombre = :nombre,
            numero_cuatrimestres = :nc
        WHERE id = :id
        """
        await self.db.execute(query, {
            "id": programa_id,
            "nombre": data["nombre"],
            "nc": data["numero_cuatrimestres"]
        })
        return await self.get_programa(programa_id)

    async def delete_programa(self, programa_id: int):
        await self.db.execute("DELETE FROM programa_estudio WHERE id = :id", {"id": programa_id})
        return {"deleted": True}

    async def create_cuatrimestre(self, numero: int, programa_id: int):
        q = """
        INSERT INTO cuatrimestre (numero, programa_id)
        VALUES (:n, :pid)
        """
        return await self.db.execute(q, {"n": numero, "pid": programa_id})

    async def list_cuatrimestres(self, programa_id: int = None):
        if programa_id:
            return await self.db.fetch_all(
                "SELECT * FROM cuatrimestre WHERE programa_id = :pid",
                {"pid": programa_id}
            )
        return await self.db.fetch_all("SELECT * FROM cuatrimestre")

    async def create_asignatura(self, nombre: str, cuatrimestre_id: int, codigo: str | None):
        q = """
        INSERT INTO asignatura (nombre, cuatrimestre_id, codigo)
        VALUES (:n, :cid, :c)
        """
        return await self.db.execute(q, {
            "n": nombre,
            "cid": cuatrimestre_id,
            "c": codigo
        })

    async def list_asignaturas(self, cuatrimestre_id: int = None):
        if cuatrimestre_id:
            return await self.db.fetch_all(
                "SELECT * FROM asignatura WHERE cuatrimestre_id = :cid",
                {"cid": cuatrimestre_id}
            )
        return await self.db.fetch_all("SELECT * FROM asignatura")

    async def create_docente(self, nombre: str, correo: str | None):
        q = """
        INSERT INTO docente (nombre, correo)
        VALUES (:n, :c)
        """
        return await self.db.execute(q, {"n": nombre, "c": correo})

    async def list_docentes(self):
        return await self.db.fetch_all("SELECT * FROM docente")

    async def create_grupo(self, nombre, asignatura_id, docente_id, cuatrimestre_id, capacidad):
        q = """
        INSERT INTO grupo (nombre, asignatura_id, docente_id, cuatrimestre_id, capacidad)
        VALUES (:n, :aid, :did, :cid, :cap)
        """
        return await self.db.execute(q, {
            "n": nombre,
            "aid": asignatura_id,
            "did": docente_id,
            "cid": cuatrimestre_id,
            "cap": capacidad
        })

    async def list_grupos(self):
        return await self.db.fetch_all("""
            SELECT g.*, a.nombre AS asignatura, d.nombre AS docente
            FROM grupo g
            JOIN asignatura a ON g.asignatura_id = a.id
            JOIN docente d ON g.docente_id = d.id
        """)

    async def create_alumno(self, nombre, matricula, cuatrimestre, correo):
        q = """
        INSERT INTO alumno (nombre, matricula, cuatrimestre, correo)
        VALUES (:n, :m, :c, :e)
        """
        return await self.db.execute(q, {
            "n": nombre,
            "m": matricula,
            "c": cuatrimestre,
            "e": correo
        })

    async def list_alumnos(self):
        return await self.db.fetch_all("SELECT * FROM alumno")

    async def add_alumno_to_grupo(self, grupo_id, alumno_id):
        q = """
        INSERT INTO grupo_alumno (grupo_id, alumno_id)
        VALUES (:gid, :aid)
        """
        return await self.db.execute(q, {"gid": grupo_id, "aid": alumno_id})

    async def list_alumnos_de_grupo(self, grupo_id):
        q = """
        SELECT a.*
        FROM alumno a
        JOIN grupo_alumno ga ON ga.alumno_id = a.id
        WHERE ga.grupo_id = :gid
        """
        return await self.db.fetch_all(q, {"gid": grupo_id})
