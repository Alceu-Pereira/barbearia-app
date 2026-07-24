from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional

class ClienteBase(BaseModel):
    nome: str
    telefone: str

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    nome: str | None = None
    telefone: str | None = None


class ClienteRegistro(BaseModel):
    nome: str
    telefone: str
    email: EmailStr
    senha: str

class ClienteLogin(BaseModel):
    email: EmailStr
    senha: str


class ClienteResponse(ClienteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: Optional[str] = None
    ativo: bool

class ClienteToken(BaseModel):
    access_token: str
    token_type: str = "bearer"
    cliente_id: int
    nome: str


class ClientePerfilUpdate(BaseModel):
    nome: str | None = None
    telefone: str | None = None
    email: EmailStr | None = None


class ClienteTrocarSenha(BaseModel):
    senha_atual: str
    senha_nova: str