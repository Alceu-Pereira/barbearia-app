from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from backend.app.database import SessionLocal
from backend.app.models.usuario import Usuario
from backend.app.services.auth_service import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

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