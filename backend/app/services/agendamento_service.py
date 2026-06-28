from sqlalchemy.orm import Session
from datetime import datetime
from backend.app.models.agendamentos import Agendamento
from backend.app.schemas.agendamento import AgendamentoCreate
from backend.app.logger import logger

def criar_agendamento(db: Session, dados: AgendamentoCreate):
    logger.info(f"Tentativa de criar agendamento - barbeiro_id: {dados.barbeiro_id}, cliente_id: {dados.cliente_id}, data_hora: {dados.data_hora}")

    # Regra 1: Não pode agendar em horário passado
    if dados.data_hora.replace(tzinfo=None) < datetime.now():
        logger.warning(f"Agendamento rejeitado - horário passado: {dados.data_hora}")
        raise ValueError("Não é possível agendar em um horário que já passou.")
    
    # Regra 2: Não pode agendar no mesmo horário com o mesmo barbeiro
    agendamento_existente = db.query(Agendamento).filter(
        Agendamento.barbeiro_id == dados.barbeiro_id,
        Agendamento.data_hora == dados.data_hora,
        Agendamento.status == "confirmado"
    ).first()

    if agendamento_existente:
        logger.warning(f"Agendamento rejeitado - horário duplicado: barbeiro_id {dados.barbeiro_id} às {dados.data_hora}")        
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

    logger.info(f"Agendamento criado com sucesso - id: {novo_agendamento.id}")
    return novo_agendamento

def listar_agendamentos(db: Session):
    logger.info("Listando todos os agendamentos")    
    return db.query(Agendamento).all()

def cancelar_agendamento(db: Session, agendamento_id: int):
    logger.info(f"Tentativa de cancelar agendamento - id: {agendamento_id}")
    agendamento = db.query(Agendamento).filter(
    Agendamento.id == agendamento_id).first()

    # Regra 3: Agendamento deve existir
    if not agendamento:
        logger.warning(f"Cancelamento rejeitado - agendamento não encontrado: id {agendamento_id}")
        raise ValueError("Agendamento não encontrado.")
    
    # Regra 4: Não pode cancelar o que já foi cancelado
    if agendamento.status == "cancelado":
        logger.warning(f"Cancelamento rejeitado - agendamento já cancelado: id {agendamento_id}")
        raise ValueError("Este agendamento já está cancelado.")
    
    agendamento.status = "cancelado"
    db.commit()
    db.refresh(agendamento)

    logger.info(f"Agendamento cancelado com sucesso - id: {agendamento_id}")
    return agendamento