from fastapi import APIRouter
from db.database import database
from schemas.schemas_cuatrimestre import CuatrimestreCreate, CuatrimestreOut

router = APIRouter()

@router.post("/cuatrimestres", tags=["Cuatrimestres"], response_model=CuatrimestreOut)
async def create_cuatrimestre(c: CuatrimestreCreate):
    q = """INSERT INTO cuatrimestre (numero, programa_id)
           VALUES (:numero, :programa_id)"""
    last_id = await database.execute(q, c.dict())
    return {"id": last_id, **c.dict()}

@router.get("/cuatrimestres", tags=["Cuatrimestres"], response_model=list[CuatrimestreOut])
async def get_cuatrimestres():
    rows = await database.fetch_all("""
        SELECT c.id, c.numero, c.programa_id, p.nombre AS programa
        FROM cuatrimestre c
        JOIN programa_estudio p ON p.id = c.programa_id
    """)
    return rows

@router.put("/cuatrimestres/{cid}", tags=["Cuatrimestres"], response_model=CuatrimestreOut)
async def update_cuatrimestre(cid: int, data: CuatrimestreCreate):
    q = """
    UPDATE cuatrimestre SET numero = :numero, programa_id = :programa_id
    WHERE id = :id
    """
    await database.execute(q, {"id": cid, **data.dict()})
    return {"id": cid, **data.dict()}

@router.delete("/cuatrimestres/{cid}", tags=["Cuatrimestres"])
async def delete_cuatrimestre(cid: int):
    await database.execute("DELETE FROM cuatrimestre WHERE id=:id", {"id": cid})
    return {"status": "deleted", "id": cid}
