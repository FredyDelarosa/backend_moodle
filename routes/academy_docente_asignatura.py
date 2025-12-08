# routers/docente_asignatura_router.py
from fastapi import APIRouter
from db.database import database
from schemas.schemas_docente import DocenteAsignaturaCreate

router = APIRouter()

@router.post("/docente-asignatura", tags=["Docente-Asignatura"])
async def add_docente_asignatura(payload: DocenteAsignaturaCreate):
    q = """
        INSERT INTO docente_asignatura (docente_id, asignatura_id)
        VALUES (:docente_id, :asignatura_id)
    """
    last_id = await database.execute(q, payload.model_dump())
    return {"id": last_id, **payload.model_dump()}

@router.get("/docente-asignatura", tags=["Docente-Asignatura"])
async def list_docente_asignatura():
    return await database.fetch_all("""
        SELECT da.id,
               d.nombre AS docente,
               a.nombre AS asignatura
        FROM docente_asignatura da
        JOIN docente d ON d.id = da.docente_id
        JOIN asignatura a ON a.id = da.asignatura_id
    """)

@router.delete("/docente-asignatura/{id}", tags=["Docente-Asignatura"])
async def delete_docente_asignatura(id: int):
    q = "DELETE FROM docente_asignatura WHERE id = :id"
    await database.execute(q, {"id": id})
    if not await database.execute(q, {"id": id}):
        return {"error": "Docente-Asignatura relationship not found"}
    return {"message": "Docente-Asignatura relationship deleted successfully"}