from pydantic import BaseModel
from typing import Optional

class GrupoCreate(BaseModel):
    nombre: str
    asignatura_id: int
    docente_id: int
    cuatrimestre_id: int
    capacidad: Optional[int] = 25
