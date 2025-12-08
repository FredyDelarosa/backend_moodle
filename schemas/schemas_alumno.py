from pydantic import BaseModel, EmailStr
from typing import Optional

class AlumnoBase(BaseModel):
    nombre: str
    matricula: str
    cuatrimestre: int
    correo: Optional[EmailStr] = None

class AlumnoCreate(AlumnoBase):
    pass

class AlumnoUpdate(AlumnoBase):
    pass

class AlumnoOut(AlumnoBase):
    id: int

    class Config:
        from_attributes = True
