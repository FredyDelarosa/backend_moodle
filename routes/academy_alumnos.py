from fastapi import APIRouter
from db.database import database

router = APIRouter()

@router.post("/alumnos", tags=["Alumnos"])
async def create_alumno(a: dict):
    q = """INSERT INTO alumno (nombre, matricula, cuatrimestre, correo)
           VALUES (:nombre, :matricula, :cuatrimestre, :correo)"""
    last_id = await database.execute(q, a)
    return {"id": last_id, **a}

@router.get("/alumnos", tags=["Alumnos"])
async def get_alumnos():
    return await database.fetch_all("SELECT * FROM alumno")

@router.put("/alumnos/{aid}", tags=["Alumnos"])
async def update_alumno(aid: int, data: dict):
    q = """UPDATE alumno SET nombre=:nombre, matricula=:matricula,
           cuatrimestre=:cuatrimestre, correo=:correo WHERE id=:id"""
    await database.execute(q, {"id": aid, **data})
    return {"id": aid, **data}

@router.delete("/alumnos/{aid}", tags=["Alumnos"])
async def delete_alumno(aid: int):
    await database.execute("DELETE FROM alumno WHERE id=:id", {"id": aid})
    return {"status": "deleted", "id": aid}
