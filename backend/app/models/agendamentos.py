from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database import Base

class Agendamento(Base):
    __tablename__ = "agendamentos"

    id = Column(Integer, primary_key=True, index=True)
    barbeiro_id = Column(Integer, ForeignKey("barbeiros.id"), nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    data_hora = Column(DateTime, nullable=False)
    status = Column(String, default="confirmado")

    barbeiro = relationship("Barbeiro")
    cliente = relationship("Cliente")