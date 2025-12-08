from fastapi import APIRouter, HTTPException
from db.database import database
from schemas.schemas_alumno import AlumnoCreate, AlumnoUpdate, AlumnoOut

router = APIRouter()

@router.post("/alumnos", tags=["Alumnos"], response_model=AlumnoOut)
async def create_alumno(a: AlumnoCreate):
    q = """
    INSERT INTO alumno (nombre, matricula, cuatrimestre, correo)
    VALUES (:nombre, :matricula, :cuatrimestre, :correo)
    """
    last_id = await database.execute(q, a.model_dump())
    return AlumnoOut(id=last_id, **a.model_dump())

@router.get("/alumnos", tags=["Alumnos"], response_model=list[AlumnoOut])
async def get_alumnos():
    rows = await database.fetch_all("SELECT * FROM alumno")
    return [AlumnoOut(**r) for r in rows]

@router.get("/alumnos/{aid}", tags=["Alumnos"], response_model=AlumnoOut)
async def get_alumno(aid: int):
    row = await database.fetch_one(
        "SELECT * FROM alumno WHERE id = :id", {"id": aid}
    )
    if not row:
        raise HTTPException(404, "Alumno no encontrado")
    return AlumnoOut(**row)

@router.put("/alumnos/{aid}", tags=["Alumnos"], response_model=AlumnoOut)
async def update_alumno(aid: int, data: AlumnoUpdate):
    q = """
    UPDATE alumno
    SET nombre=:nombre, matricula=:matricula,
        cuatrimestre=:cuatrimestre, correo=:correo
    WHERE id=:id
    """
    values = data.model_dump()
    await database.execute(q, {"id": aid, **values})
    return AlumnoOut(id=aid, **values)

@router.delete("/alumnos/{aid}", tags=["Alumnos"])
async def delete_alumno(aid: int):
    await database.execute("DELETE FROM alumno WHERE id=:id", {"id": aid})
    return {"status": "deleted", "id": aid}
