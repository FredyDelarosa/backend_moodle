from fastapi import APIRouter
from db.database import database

router = APIRouter()

@router.post("/asignaturas", tags=["Asignaturas"])
async def create_asignatura(a: dict):
    q = """INSERT INTO asignatura (nombre, cuatrimestre_id, codigo)
           VALUES (:nombre, :cuatrimestre_id, :codigo)"""
    last_id = await database.execute(q, a)
    return {"id": last_id, **a}

@router.get("/asignaturas", tags=["Asignaturas"])
async def get_asignaturas():
    return await database.fetch_all("""
        SELECT a.*, c.numero AS cuatrimestre
        FROM asignatura a
        JOIN cuatrimestre c ON c.id = a.cuatrimestre_id
    """)

@router.put("/asignaturas/{aid}", tags=["Asignaturas"])
async def update_asignatura(aid: int, data: dict):
    q = """
    UPDATE asignatura
    SET nombre=:nombre, cuatrimestre_id=:cuatrimestre_id, codigo=:codigo
    WHERE id=:id
    """
    await database.execute(q, {"id": aid, **data})
    return {"id": aid, **data}

@router.delete("/asignaturas/{aid}", tags=["Asignaturas"])
async def delete_asignatura(aid: int):
    await database.execute("DELETE FROM asignatura WHERE id=:id", {"id": aid})
    return {"status": "deleted", "id": aid}
