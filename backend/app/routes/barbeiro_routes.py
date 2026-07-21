from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import SessionLocal
from backend.app.schemas.barbeiro import BarbeiroCreate, BarbeiroUpdate, BarbeiroResponse
from backend.app.services import barbeiro_service
from backend.app.services.seguranca import verificar_admin
from backend.app.models.usuario import Usuario
from typing import List

router = APIRouter(
    prefix="/barbeiros",
    tags=["Barbeiros"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=BarbeiroResponse)
def criar_barbeiro(dados: BarbeiroCreate, db: Session = Depends(get_db), usuario: Usuario = Depends(get_db)):
    try:
        return barbeiro_service.criar_barbeiro(db, dados)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/", response_model=List[BarbeiroResponse])
def listar_barbeiros(db: Session = Depends(get_db)):
    return barbeiro_service.listar_barbeiros(db)

@router.get("/{barbeiro_id}", response_model=BarbeiroResponse)
def buscar_barbeiro(barbeiro_id: int, db: Session = Depends(get_db)):
    try:
        return barbeiro_service.buscar_barbeiro(db, barbeiro_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.put("/{barbeiro_id}", response_model=BarbeiroResponse)
def atualizar_barbeiro(barbeiro_id: int, dados: BarbeiroUpdate, db: Session = Depends(get_db), usuario: Usuario = Depends(verificar_admin)):
    try:
        return barbeiro_service.atualizar_barbeiro(db, barbeiro_id, dados)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.delete("/{barbeiro_id}")
def deletar_barbeiro(barbeiro_id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(verificar_admin)):
    try:
        return barbeiro_service.deletar_barbeiro(db, barbeiro_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    