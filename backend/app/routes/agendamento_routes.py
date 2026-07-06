from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import SessionLocal
from backend.app.schemas.agendamento import AgendamentoCreate, AgendamentoResponse
from backend.app.services import agendamento_service
from backend.app.services.seguranca import usuario_ou_cliente
from typing import List

router = APIRouter(
    prefix="/agendamentos",
    tags=["Agendamentos"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=AgendamentoResponse)
def criar_agendamento(
    dados: AgendamentoCreate,
    db: Session = Depends(get_db),
    usuario = Depends(usuario_ou_cliente)
):
    try:
        return agendamento_service.criar_agendamento(db, dados)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[AgendamentoResponse])
def listar_agendamentos(db: Session = Depends(get_db)):
    return agendamento_service.listar_agendamentos(db)

@router.patch("/{agendamento_id}/cancelar", response_model=AgendamentoResponse)
def cancelar_agendamento(
    agendamento_id: int,
    db: Session = Depends(get_db),
    usuario = Depends(usuario_ou_cliente)
):
    try:
        return agendamento_service.cancelar_agendamento(db, agendamento_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))