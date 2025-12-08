from fastapi import APIRouter
from db.database import database
from schemas.schemas_docente import DocenteCreate

router = APIRouter()

@router.post("/docentes", tags=["Docentes"])
async def create_docente(d: DocenteCreate):
    q = """INSERT INTO docente (nombre, correo)
           VALUES (:nombre, :correo)"""
    last_id = await database.execute(q, d.dict())
    return { "id": last_id, **d.dict() }

@router.get("/docentes", tags=["Docentes"])
async def get_docentes():
    return await database.fetch_all("SELECT * FROM docente")

@router.put("/docentes/{did}", tags=["Docentes"])
async def update_docente(did: int, data: DocenteCreate):
    q = """UPDATE docente
           SET nombre=:nombre, correo=:correo
           WHERE id=:id"""
    await database.execute(q, {"id": did, **data.dict()})
    return { "id": did, **data.dict() }

@router.delete("/docentes/{did}", tags=["Docentes"])
async def delete_docente(did: int):
    await database.execute(
        "DELETE FROM docente WHERE id=:id",
        {"id": did}
    )
    return {"status": "deleted", "id": did}
