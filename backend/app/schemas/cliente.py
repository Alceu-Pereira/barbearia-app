from pydantic import BaseModel, ConfigDict

class ClienteBase(BaseModel):
    nome: str
    telefone: str

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    nome: str | None = None
    telfone: str | None = None

class ClienteResponse(ClienteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    