from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import SessionLocal
from backend.app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse
from backend.app.services import cliente_service
from backend.app.services.seguranca import usuario_atual
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


@router.post("/", response_model=ClienteResponse)
def criar_cliente(
    dados: ClienteCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(usuario_atual)
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
    usuario: Usuario = Depends(usuario_atual)
):
    try:
        return cliente_service.atualizar_cliente(db, cliente_id, dados)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{cliente_id}")
def deletar_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(usuario_atual)
):
    try:
        return cliente_service.deletar_cliente(db, cliente_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))