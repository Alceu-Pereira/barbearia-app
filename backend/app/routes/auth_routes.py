from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.app.database import SessionLocal
from backend.app.models.usuario import Usuario
from backend.app.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioLogin, Token
from backend.app.services.auth_service import gerar_hash_senha, autenticar_usuario, criar_token

router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/cadastro", response_model=UsuarioResponse)
def cadastrar_usuario(dados: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.email == dados.email).first()

    if usuario_existente:
        raise HTTPException(status_code=400, detail="Este email já está cadastrado.")
    
    novo_usuario = Usuario(
        nome = dados.nome,
        email = dados.email,
        senha_hash = gerar_hash_senha(dados.senha)
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return novo_usuario

@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = autenticar_usuario(db, form.username, form.password)

    if not usuario:
        raise HTTPException(status_code=401, detail="Email ou senha incorretos.")
    
    token = criar_token(usuario.email)

    return {"access_token": token, "token_type": "bearer"}