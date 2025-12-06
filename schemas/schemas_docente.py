from pydantic import BaseModel, EmailStr
from typing import List, Optional

class DocenteCreate(BaseModel):
    nombre: str
    correo: Optional[EmailStr] = None
    asignatura_ids: Optional[List[int]] = []
