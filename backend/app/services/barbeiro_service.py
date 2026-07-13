from sqlalchemy.orm import Session
from backend.app.models.barbeiro import Barbeiro
from backend.app.schemas.barbeiro import BarbeiroCreate, BarbeiroUpdate
from backend.app.logger import logger

def criar_barbeiro(db: Session, dados: BarbeiroCreate):
    logger.info(f"Criando barbeiro: {dados.nome}")

    barbeiro_existe = db.query(Barbeiro).filter(
        Barbeiro.nome == dados.nome
    ).first()

    if barbeiro_existe:
        raise ValueError("Já existe um barbeiro com esse nome.")
    
    novo_barbeiro = Barbeiro(
        nome = dados.nome,
        especialidade = dados.especialidade
    )

    db.add(novo_barbeiro)
    db.commit()
    db.refresh(novo_barbeiro)

    logger.info(f"Barbeiro criado com sucesso - id: {novo_barbeiro.id}")
    return novo_barbeiro


def listar_barbeiros(db: Session):
    logger.info(f"Listando todos os barbeiros")
    return db.query(Barbeiro).filter(Barbeiro.ativo == True).all()

def buscar_barbeiro(db: Session, barbeiro_id: int):
    barbeiro = db.query(Barbeiro).filter(Barbeiro.id == barbeiro_id).first()

    if not barbeiro:
        raise ValueError("Barbeiro não encontrado.")
    
    return barbeiro


def atualizar_barbeiro(db: Session, barbeiro_id: int, dados: BarbeiroUpdate):
    logger.info(f"Atualizado barbeiro - id: {barbeiro_id}")

    barbeiro = buscar_barbeiro(db, barbeiro_id)

    if dados.nome is not None:
        barbeiro.nome = dados.nome

    if dados.especialidade is not None:
        barbeiro.especialidade = dados.especialidade
    
    if dados.ativo is not None:
        barbeiro.ativo = dados.ativo

    db.commit()
    db.refresh(barbeiro)

    logger.info(f"Barbeiro atualizado com sucesso - id: {barbeiro_id}")
    return barbeiro

def deletar_barbeiro(db: Session, barbeiro_id: int):
    logger.info(f"Deletando barbeiro - id: {barbeiro_id}")

    barbeiro = buscar_barbeiro(db, barbeiro_id)

    db.delete(barbeiro)
    db.commit()

    logger.info(f"Barbeiro deletado com sucesso - id: {barbeiro_id}")
    return {"mensagem": "Barbeiro deletado com sucesso."}

