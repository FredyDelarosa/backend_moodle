from fastapi import APIRouter, HTTPException
from db.database import database

router = APIRouter()

@router.post("/programas", tags=["Programas"])
async def create_programa(p: dict):
    q = """INSERT INTO programa_estudio (nombre, numero_cuatrimestres)
           VALUES (:nombre, :cuatrimestres)"""
    last_id = await database.execute(q, {"nombre": p["nombre"], "cuatrimestres": p["numero_cuatrimestres"]})
    return { "id": last_id, **p }

@router.get("/programas", tags=["Programas"])
async def get_programas():
    return await database.fetch_all("SELECT * FROM programa_estudio")

@router.get("/programas/{pid}", tags=["Programas"])
async def get_programa(pid: int):
    p = await database.fetch_one("SELECT * FROM programa_estudio WHERE id = :id", {"id": pid})
    if not p:
        raise HTTPException(404, "Programa no encontrado")
    return p

@router.put("/programas/{pid}", tags=["Programas"])
async def update_programa(pid: int, data: dict):
    q = """
    UPDATE programa_estudio SET nombre = :nombre, numero_cuatrimestres = :cuatrimestres
    WHERE id = :id"""
    await database.execute(q, {
        "id": pid, "nombre": data["nombre"], "cuatrimestres": data["numero_cuatrimestres"]
    })
    return {"id": pid, **data}

@router.delete("/programas/{pid}", tags=["Programas"])
async def delete_programa(pid: int):
    await database.execute("DELETE FROM programa_estudio WHERE id = :id", {"id": pid})
    return {"status": "deleted", "id": pid}
