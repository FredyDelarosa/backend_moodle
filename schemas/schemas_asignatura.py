from pydantic import BaseModel
from typing import Optional

class AsignaturaBase(BaseModel):
    nombre: str
    cuatrimestre_id: int
    codigo: Optional[str] = None

class AsignaturaCreate(AsignaturaBase):
    pass

class AsignaturaOut(AsignaturaBase):
    id: int
