from pydantic import BaseModel, EmailStr
from typing import Optional

class AlumnoCreate(BaseModel):
    nombre: str
    matricula: str
    cuatrimestre: int
    correo: Optional[EmailStr] = None
