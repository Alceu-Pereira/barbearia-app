from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from backend.app.database import SessionLocal
from backend.app.models.usuario import Usuario
from backend.app.models.cliente import Cliente
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="clientes/login", auto_error=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def usuario_atual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    erro_credenciais = HTTPException(
        status_code=401,
        detail="Não foi possível validar as credenciais."
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if email is None:
            raise erro_credenciais

    except JWTError:
        raise erro_credenciais

    usuario = db.query(Usuario).filter(Usuario.email == email).first()

    if usuario is None:
        raise erro_credenciais

    return usuario


def usuario_ou_cliente(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=False)),
    db: Session = Depends(get_db)
):
    erro_credenciais = HTTPException(
        status_code=401,
        detail="Não foi possível validar as credenciais."
    )

    if not token:
        raise erro_credenciais

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if email is None:
            raise erro_credenciais

        # Verifica se é admin
        usuario = db.query(Usuario).filter(Usuario.email == email).first()
        if usuario:
            return usuario

        # Verifica se é cliente
        cliente = db.query(Cliente).filter(Cliente.email == email).first()
        if cliente:
            return cliente

        raise erro_credenciais

    except JWTError:
        raise erro_credenciais
    
