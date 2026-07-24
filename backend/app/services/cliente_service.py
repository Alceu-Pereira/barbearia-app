from sqlalchemy.orm import Session
from backend.app.models.cliente import Cliente
from backend.app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteRegistro, ClientePerfilUpdate, ClienteTrocarSenha
from backend.app.logger import logger
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, UTC
from dotenv import load_dotenv
import os

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
EXPIRACAO_MINUTOS = 60

def gerar_hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)

def verificar_senha(senha_texto:str, senha_hash: str) -> bool:
    return pwd_context.verify(senha_texto, senha_hash)


def criar_token_cliente(cliente_id: int, email: str) -> str:
    expira_em = datetime.now(UTC) + timedelta(minutes=EXPIRACAO_MINUTOS)
    dados = {"sub": email, "cliente_id": cliente_id, "exp": expira_em}
    return jwt.encode(dados, SECRET_KEY, algorithm=ALGORITHM)

def registrar_cliente(db: Session, dados: ClienteRegistro):
    logger.info(f"Tentativa de registro de cliente: {dados.email}")

    # Regra 1: Email único
    email_existente = db.query(Cliente).filter(Cliente.email == dados.email).first()

    if email_existente:
        raise ValueError("Este email já está cadastrado.")
    
    # Regra 2: Telefone único
    telefone_existente = db.query(Cliente).filter(Cliente.telefone == dados.telefone).first()

    if telefone_existente:
        raise ValueError("Este telefone já está cadastrado.")
    
    novo_cliente = Cliente(
        nome = dados.nome,
        telefone = dados.telefone,
        email = dados.email,
        senha_hash = gerar_hash_senha(dados.senha)
    )

    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)

    logger.info(f"Cliente registrado com sucesso - id: {novo_cliente.id}")

    return novo_cliente

def autenticar_cliente(db: Session, email: str, senha: str):
    cliente = db.query(Cliente).filter(Cliente.email == email).first()

    if not cliente:
        logger.warning(f"Login cliente - email não encontrado: {email}")
        return None

    if not cliente.senha_hash:
        logger.warning(f"Login cliente - cliente sem senha cadastrada: {email}")
        return None

    if not verificar_senha(senha, cliente.senha_hash):
        logger.warning(f"Login cliente - senha incorreta: {email}")
        return None
    
    logger.info(f"Login cliente realizado com sucesso: {email}")
    return cliente

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
        cliente.telefone = dados.telefone

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


def atualizar_meu_perfil(db: Session, cliente: Cliente, dados: ClientePerfilUpdate):
    if dados.email is not None and dados.email != cliente.email:
        email_existente = db.query(Cliente).filter(Cliente.email == dados.email).first()
        if email_existente:
            raise ValueError("Este email já está cadastrado.")
        cliente.email = dados.email

    if dados.nome is not None:
        cliente.nome = dados.nome

    if dados.telefone is not None and dados.telefone != cliente.telefone:
        telefone_existente = db.query(Cliente).filter(Cliente.telefone == dados.telefone).first()
        if telefone_existente:
            raise ValueError("Este telefone já está cadastrado.")
        cliente.telefone = dados.telefone

    db.commit()
    db.refresh(cliente)

    return cliente

def trocar_senha(db: Session, cliente: Cliente, dados: ClienteTrocarSenha):
    if not verificar_senha(dados.senha_atual, cliente.senha_hash):
        raise ValueError("Senha atual incorreta.")

    cliente.senha_hash = gerar_hash_senha(dados.senha_nova)

    db.commit()
    db.refresh(cliente)

    return cliente
    