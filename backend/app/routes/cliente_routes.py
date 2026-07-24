from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.app.database import SessionLocal
from backend.app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse, ClienteRegistro, ClienteToken, ClienteTrocarSenha, ClientePerfilUpdate
from backend.app.services import cliente_service
from backend.app.services.seguranca import verificar_admin, admin_ou_cliente
from backend.app.models.usuario import Usuario
from typing import List

router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/registro", response_model=ClienteResponse)
def registrar_cliente(dados: ClienteRegistro, db: Session = Depends(get_db)):
    try:
        return cliente_service.registrar_cliente(db, dados)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=ClienteToken)
def login_cliente(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    cliente = cliente_service.autenticar_cliente(db, form.username, form.password)

    if not cliente:
        raise HTTPException(status_code=401, detail="Email ou senha incorretos.")
    
    token = cliente_service.criar_token_cliente(cliente.id, cliente.email)

    return {
        "access_token": token,
        "token_type": "bearer",
        "cliente_id": cliente.id,
        "nome": cliente.nome,
    }


@router.get("/meus-agendamentos/{cliente_id}")
def meus_agendamentos(cliente_id: int, db: Session = Depends(get_db)):
    from backend.app.models.agendamento import Agendamento
    agendamentos = db.query(Agendamento).filter(
        Agendamento.cliente_id == cliente_id
    ).all()

    return agendamentos

@router.post("/", response_model=ClienteResponse)
def criar_cliente(
    dados: ClienteCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(verificar_admin)
):
    try:
        return cliente_service.criar_cliente(db, dados)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[ClienteResponse])
def listar_clientes(db: Session = Depends(get_db)):
    return cliente_service.listar_clientes(db)


@router.get("/{cliente_id}", response_model=ClienteResponse)
def buscar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    try:
        return cliente_service.buscar_cliente(db, cliente_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{cliente_id}", response_model=ClienteResponse)
def atualizar_cliente(
    cliente_id: int,
    dados: ClienteUpdate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(verificar_admin)
):
    try:
        return cliente_service.atualizar_cliente(db, cliente_id, dados)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{cliente_id}")
def deletar_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(verificar_admin)
):
    try:
        return cliente_service.deletar_cliente(db, cliente_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

@router.put("/meu-perfil", response_model=ClienteResponse)
def atualizar_meu_perfil(dados: ClientePerfilUpdate,
                         db: Session = Depends(get_db),
                         cliente = Depends(admin_ou_cliente)):
    try:
        return cliente_service.atualizar_meu_perfil(db, cliente, dados)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/trocar-senha", response_model=ClienteResponse)
def trocar_minha_senha(dados: ClienteTrocarSenha,
                 db: Session = Depends(get_db),
                 cliente = Depends(admin_ou_cliente)):
    try:
        return cliente_service.trocar_senha(db, cliente, dados)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))