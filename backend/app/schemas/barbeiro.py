from pydantic import BaseModel, ConfigDict

class BarbeiroBase(BaseModel):
    nome: str
    especialidade: str

class BarbeiroCreate(BarbeiroBase):
    pass

class BarbeiroUpdate(BaseModel):
    nome: str | None = None
    especialidade: str | None = None
    ativo: bool | None = None

class BarbeiroResponse(BarbeiroBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ativo: bool
