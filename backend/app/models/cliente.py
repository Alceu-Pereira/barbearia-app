from sqlalchemy import Column, Integer, String, Boolean
from backend.app.database import Base

class Cliente(Base):

    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)
    senha_hash = Column(String, nullable=True)
    ativo = Column(Boolean, default=True)