from pydantic import BaseModel
from typing import Optional

class AsignaturaCreate(BaseModel):
    nombre: str
    cuatrimestre_id: int
    codigo: Optional[str] = None
