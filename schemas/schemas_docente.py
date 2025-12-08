from pydantic import BaseModel, EmailStr
from typing import Optional

class DocenteCreate(BaseModel):
    nombre: str
    correo: Optional[EmailStr] = None

class DocenteAsignaturaCreate(BaseModel):
    docente_id: int
    asignatura_id: int