from sqlalchemy.orm import Session
from backend.app.models.cliente import Cliente
from backend.app.schemas.cliente import ClienteCreate, ClienteUpdate
from backend.app.logger import logger

def criar_cliente(db: Session, dados: ClienteCreate):
    logger.info(f"Criando cliente: {dados.nome}")

    cliente_existente = db.query(Cliente).filter(Cliente.telefone == dados.telefone).first()

    if cliente_existente:
        raise ValueError("Já existe um cliente com esse telefone.")
    
    novo_cliente = Cliente(
        nome=dados.nome,
        telefone=dados.telefone
    )

    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)

    logger.info(f"Cliente criado com sucesso - id: {novo_cliente.id}")
    return novo_cliente

def listar_clientes(db: Session):
    logger.info("Listando todos os clientes")
    return db.query(Cliente).all()

def buscar_cliente(db: Session, cliente_id: int):
    cliente = db.query(Cliente).filter(
        Cliente.id == cliente_id
    ).first()

    if not cliente:
        raise ValueError("Cliente não encontrado.")
    
    return cliente

def atualizar_cliente(db: Session, cliente_id: int, dados: ClienteUpdate):
    logger.info(f"Atualizando cliente - id: {cliente_id}")

    cliente = buscar_cliente(db, cliente_id)

    if dados.nome is not None:
        cliente.nome = dados.nome
    if dados.telefone is not None:
        cliente.telefone = dados.telfone

    db.commit()
    db.refresh(cliente)

    logger.info(f"Cliente atualizado com sucesso - id: {cliente_id}")
    return cliente

def deletar_cliente(db: Session, cliente_id: int):
    logger.info(f"Deletando cliente - id: {cliente_id}")

    cliente = buscar_cliente(db, cliente_id)

    db.delete(cliente)
    db.commit()

    logger.info(f"Cliente deletado com sucesso - id: {cliente_id}")
    return {"mensagem": "Cliente deletado com sucesso."}


