from pydantic import BaseModel

class ProgramaBase(BaseModel):
    nombre: str
    numero_cuatrimestres: int

class ProgramaCreate(ProgramaBase):
    pass

class ProgramaUpdate(ProgramaBase):
    pass

class ProgramaOut(ProgramaBase):
    id: int

    class Config:
        from_attributes = True
