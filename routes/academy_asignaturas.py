from fastapi import APIRouter, HTTPException
from db.database import database
from schemas.schemas_asignatura import AsignaturaCreate, AsignaturaOut

router = APIRouter()

@router.post("/asignaturas", tags=["Asignaturas"], response_model=AsignaturaOut)
async def create_asignatura(a: AsignaturaCreate):
    q = """INSERT INTO asignatura (nombre, cuatrimestre_id, codigo)
           VALUES (:nombre, :cuatrimestre_id, :codigo)"""
    last_id = await database.execute(q, a.model_dump())
    return {"id": last_id, **a.model_dump()}

@router.get("/asignaturas", tags=["Asignaturas"])
async def get_asignaturas():
    return await database.fetch_all("""
        SELECT a.*, c.numero AS cuatrimestre
        FROM asignatura a
        JOIN cuatrimestre c ON c.id = a.cuatrimestre_id
    """)

@router.put("/asignaturas/{aid}", tags=["Asignaturas"], response_model=AsignaturaOut)
async def update_asignatura(aid: int, data: AsignaturaCreate):
    q = """
    UPDATE asignatura
    SET nombre=:nombre, cuatrimestre_id=:cuatrimestre_id, codigo=:codigo
    WHERE id=:id
    """
    payload = data.model_dump()
    await database.execute(q, {"id": aid, **payload})
    return {"id": aid, **payload}

@router.delete("/asignaturas/{aid}", tags=["Asignaturas"])
async def delete_asignatura(aid: int):
    await database.execute("DELETE FROM asignatura WHERE id=:id", {"id": aid})
    return {"status": "deleted", "id": aid}
