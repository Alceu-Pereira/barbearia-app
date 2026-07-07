from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database import Base

class Agendamentos(Base):
    __tablename__ = "agendamentos"

    id = Column(Integer, primary_key=True, index=True)
    barbeiro_id = Column(Integer, ForeignKey("barbeiros.id"), nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    data_hora = Column(DateTime, nullable=False)
    status = Column(String, default="confirmado")

    # Relationship faz com que barbeiro_id aponte para a tabela barbeiros e busque o "barbeiros.id"
    barbeiro = relationship("Barbeiro")
    cliente = relationship("Cliente")