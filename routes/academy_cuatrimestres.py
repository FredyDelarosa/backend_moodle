from fastapi import APIRouter
from db.database import database

router = APIRouter()

@router.post("/cuatrimestres", tags=["Cuatrimestres"])
async def create_cuatrimestre(c: dict):
    q = """INSERT INTO cuatrimestre (numero, programa_id)
           VALUES (:numero, :programa_id)"""
    last_id = await database.execute(q, c)
    return {"id": last_id, **c}

@router.get("/cuatrimestres", tags=["Cuatrimestres"])
async def get_cuatrimestres():
    return await database.fetch_all("""
        SELECT c.*, p.nombre AS programa
        FROM cuatrimestre c
        JOIN programa_estudio p ON p.id = c.programa_id
    """)

@router.put("/cuatrimestres/{cid}", tags=["Cuatrimestres"])
async def update_cuatrimestre(cid: int, data: dict):
    q = """
    UPDATE cuatrimestre SET numero = :numero, programa_id = :programa_id
    WHERE id = :id"""
    await database.execute(q, {"id": cid, **data})
    return {"id": cid, **data}

@router.delete("/cuatrimestres/{cid}", tags=["Cuatrimestres"])
async def delete_cuatrimestre(cid: int):
    await database.execute("DELETE FROM cuatrimestre WHERE id=:id", {"id": cid})
    return {"status": "deleted", "id": cid}
