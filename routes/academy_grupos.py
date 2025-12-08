from fastapi import APIRouter, HTTPException
from db.database import database
from schemas.schemas_grupo import (
    GrupoCreate, GrupoUpdate, GrupoOut, GrupoAlumnoAdd
)

router = APIRouter()

@router.post("/grupos", tags=["Grupos"], response_model=GrupoOut)
async def create_grupo(g: GrupoCreate):
    q = """
        INSERT INTO grupo (nombre, asignatura_id, docente_id,
                           cuatrimestre_id, capacidad)
        VALUES (:nombre, :asignatura_id, :docente_id,
                :cuatrimestre_id, :capacidad)
    """
    last_id = await database.execute(q, g.dict())
    return GrupoOut(id=last_id, **g.dict())


@router.get("/grupos", tags=["Grupos"])
async def get_grupos():
    return await database.fetch_all("""
        SELECT g.*, a.nombre AS asignatura, d.nombre AS docente
        FROM grupo g
        JOIN asignatura a ON a.id = g.asignatura_id
        JOIN docente d ON d.id = g.docente_id
    """)


@router.put("/grupos/{gid}", tags=["Grupos"], response_model=GrupoOut)
async def update_grupo(gid: int, data: GrupoUpdate):
    q = """
        UPDATE grupo SET nombre=:nombre, asignatura_id=:asignatura_id,
        docente_id=:docente_id, cuatrimestre_id=:cuatrimestre_id,
        capacidad=:capacidad WHERE id=:id
    """
    await database.execute(q, {"id": gid, **data.dict()})
    return GrupoOut(id=gid, **data.dict())


@router.delete("/grupos/{gid}", tags=["Grupos"])
async def delete_grupo(gid: int):
    await database.execute("DELETE FROM grupo WHERE id=:id", {"id": gid})
    return {"status": "deleted", "id": gid}

@router.post("/grupos/{gid}/alumnos", tags=["Grupos"])
async def add_student_to_group(gid: int, data: GrupoAlumnoAdd):
    grupo = await database.fetch_one(
        "SELECT id FROM grupo WHERE id=:id", {"id": gid}
    )
    if not grupo:
        raise HTTPException(400, "Grupo inexistente")

    alumno = await database.fetch_one(
        "SELECT id FROM alumno WHERE id=:id", {"id": data.alumno_id}
    )
    if not alumno:
        raise HTTPException(400, "Alumno inexistente")

    q = """INSERT INTO grupo_alumno (grupo_id, alumno_id)
           VALUES (:grupo_id, :alumno_id)"""
    last_id = await database.execute(
        q,
        {"grupo_id": gid, "alumno_id": data.alumno_id}
    )
    return {"id": last_id, "grupo_id": gid, "alumno_id": data.alumno_id}



@router.get("/grupos/{gid}/alumnos", tags=["Grupos"])
async def list_students_in_group(gid: int):
    return await database.fetch_all("""
        SELECT a.id, a.nombre, a.matricula, a.correo
        FROM alumno a
        JOIN grupo_alumno ga ON ga.alumno_id = a.id
        WHERE ga.grupo_id = :gid
    """, {"gid": gid})

@router.delete("/grupos/{gid}/alumnos/{aid}", tags=["Grupos"])
async def remove_student_from_group(gid: int, aid: int):
    await database.execute("""
        DELETE FROM grupo_alumno
        WHERE grupo_id=:gid AND alumno_id=:aid
    """, {"gid": gid, "aid": aid})
    return {"status": "removed", "grupo_id": gid, "alumno_id": aid}
