from sqlalchemy import Column, Integer, String, Boolean
from backend.app.database import Base

class Usuario(Base):
    
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    ativo = Column(Boolean, default=True)