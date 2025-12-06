from fastapi import APIRouter
from db.database import database

router = APIRouter()

@router.post("/docente-asignatura", tags=["Docente-Asignatura"])
async def add_docente_asignatura(data: dict):
    q = """INSERT INTO docente_asignatura (docente_id, asignatura_id)
           VALUES (:docente_id, :asignatura_id)"""
    last_id = await database.execute(q, data)
    return {"id": last_id, **data}

@router.get("/docente-asignatura", tags=["Docente-Asignatura"])
async def list_docente_asignatura():
    return await database.fetch_all("""
        SELECT da.id, d.nombre AS docente, a.nombre AS asignatura
        FROM docente_asignatura da
        JOIN docente d ON d.id = da.docente_id
        JOIN asignatura a ON a.id = da.asignatura_id
    """)
