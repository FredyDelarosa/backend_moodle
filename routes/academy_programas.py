from fastapi import APIRouter, HTTPException
from db.database import database
from schemas.schemas_programa import (
    ProgramaCreate, ProgramaUpdate, ProgramaOut
)

router = APIRouter()

@router.post("/programas", response_model=ProgramaOut, tags=["Programas"])
async def create_programa(p: ProgramaCreate):
    q = """INSERT INTO programa_estudio (nombre, numero_cuatrimestres)
           VALUES (:nombre, :cuatrimestres)"""
    last_id = await database.execute(q, {
        "nombre": p.nombre,
        "cuatrimestres": p.numero_cuatrimestres
    })
    return ProgramaOut(id=last_id, **p.model_dump())


@router.get("/programas", response_model=list[ProgramaOut], tags=["Programas"])
async def get_programas():
    rows = await database.fetch_all("SELECT * FROM programa_estudio")
    return [ProgramaOut(**r) for r in rows]


@router.get("/programas/{pid}", response_model=ProgramaOut, tags=["Programas"])
async def get_programa(pid: int):
    p = await database.fetch_one(
        "SELECT * FROM programa_estudio WHERE id = :id",
        {"id": pid}
    )
    if not p:
        raise HTTPException(404, "Programa no encontrado")
    return ProgramaOut(**p)


@router.put("/programas/{pid}", response_model=ProgramaOut, tags=["Programas"])
async def update_programa(pid: int, data: ProgramaUpdate):
    q = """
    UPDATE programa_estudio
    SET nombre = :nombre, numero_cuatrimestres = :cuatrimestres
    WHERE id = :id
    """
    await database.execute(q, {
        "id": pid,
        "nombre": data.nombre,
        "cuatrimestres": data.numero_cuatrimestres
    })
    return ProgramaOut(id=pid, **data.model_dump())


@router.delete("/programas/{pid}", tags=["Programas"])
async def delete_programa(pid: int):
    await database.execute(
        "DELETE FROM programa_estudio WHERE id = :id",
        {"id": pid}
    )
    return {"status": "deleted", "id": pid}
