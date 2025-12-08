from pydantic import BaseModel

class CuatrimestreCreate(BaseModel):
    numero: int
    programa_id: int

class CuatrimestreOut(BaseModel):
    id: int
    numero: int
    programa_id: int
    programa: str | None = None