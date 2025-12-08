from pydantic import BaseModel
from typing import Optional

class GrupoBase(BaseModel):
    nombre: str
    asignatura_id: int
    docente_id: int
    cuatrimestre_id: int
    capacidad: Optional[int] = 25

class GrupoCreate(GrupoBase):
    pass

class GrupoUpdate(GrupoBase):
    pass

class GrupoOut(GrupoBase):
    id: int

    class Config:
        from_attributes = True

class GrupoAlumnoAdd(BaseModel):
    alumno_id: int
