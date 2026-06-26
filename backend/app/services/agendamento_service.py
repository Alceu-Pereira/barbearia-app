from sqlalchemy.orm import Session
from datetime import datetime
from backend.app.models.agendamentos import Agendamento
from backend.app.schemas.agendamento import AgendamentoCreate

def criar_agendamento(db: Session, dados: AgendamentoCreate):
    
    # Regra 1: Não pode agendar em horário passado
    if dados.data_hora < datetime.now():
        raise ValueError("Não é possível agendar em um horário que já passou.")
    
    # Regra 2: Não pode agendar no mesmo horário com o mesmo barbeiro
    agendamento_existente = db.query(Agendamento).filter(
        Agendamento.barbeiro_id == dados.barbeiro_id,
        Agendamento.data_hora == dados.data_hora,
        Agendamento.status == "confirmado"
    ).first()

    if agendamento_existente:
        raise ValueError("Este barbeiro já possui um agendamento neste horário.")
    
    # Tudo certo - cria o agendamento
    novo_agendamento = Agendamento(
        barbeiro_id = dados.barbeiro_id,
        cliente_id = dados.cliente_id,
        data_hora = dados.data_hora,
        status = "confirmado"
    )

    db.add(novo_agendamento)
    db.commit()
    db.refresh(novo_agendamento)

    return novo_agendamento

def listar_agendamentos(db: Session):
    return db.query(Agendamento).all()

def cancelar_agendamento(db: Session, agendamento_id: int):
    agendamento = db.get(Agendamento, agendamento_id)

    # Regra 3: Agendamento deve existir
    if not agendamento:
        raise ValueError("Agendamento não encontrado.")
    
    # Regra 4: Não pode cancelar o que já foi cancelado
    if agendamento.status == "cancelado":
        raise ValueError("Este agendamento já está cancelado.")
    
    agendamento.status = "cancelado"
    db.commit()
    db.refresh(agendamento)

    return agendamento