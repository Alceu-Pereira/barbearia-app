from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from backend.app.models.usuario import Usuario
from backend.app.logger import logger
from dotenv import load_dotenv
import os

load_dotenv()

# Configuração do hash da senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuração do JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
EXPIRACAO_MINUTOS = 60

def gerar_hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)

def verificar_senha(senha_texto: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha_texto, senha_hash)

def criar_token(email: str) -> str:
    expira_em = datetime.utcnow() + timedelta(minutes=EXPIRACAO_MINUTOS)
    dados = {"sub": email, "exp": expira_em}
    return jwt.encode(dados, SECRET_KEY, algorithm=ALGORITHM)

def autenticar_usuario(db: Session, email: str, senha: str):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()

    if not usuario:
        logger.warning(f"Tentativa de login - usuario nao encontrado: {email}")
        return None
    
    if not verificar_senha(senha, usuario.senha_hash):
        logger.warning(f"Tentativa de login - senha incorreta: {email}")
        return None
    
    logger.info(f"Login realizado com sucesso: {email}")
    return usuario

