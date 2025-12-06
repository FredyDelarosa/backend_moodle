from pydantic import BaseModel

class ProgramaCreate(BaseModel):
    nombre: str
    numero_cuatrimestres: int

class ProgramaOut(BaseModel):
    id: int
    nombre: str
    numero_cuatrimestres: int
