from sqlalchemy import Column, Integer, String, Boolean
from backend.app.database import Base

# Model 1 - Barbeiro
# Tabela Barbeiro no banco de dados que herda de base.
class Barbeiro(Base):

    # Nome da tabela no banco de dados
    __tablename__ = "barbeiros"

    # Colunas da tabela no banco de dados
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    especialidade = Column(String, nullable=False)
    ativo = Column(Boolean, default=True)


