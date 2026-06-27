import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from backend.app.services.agendamento_service import (
    criar_agendamento,
    listar_agendamentos,
    cancelar_agendamento
)
from backend.app.schemas.agendamento import AgendamentoCreate
from backend.app.models import barbeiro, cliente, agendamentos

# FÁBRICA DE DADOS FALSOS
def make_dados(horas_futuras=24):
    return AgendamentoCreate(
        barbeiro_id=1,
        cliente_id=1,
        data_hora=datetime.now() + timedelta(hours=horas_futuras)
    )

def make_agendamento_fake(status="confirmado"):
    agendamento = MagicMock()
    agendamento.id = 1
    agendamento.barbeiro_id = 1
    agendamento.cliente_id = 1
    agendamento.data_hora = datetime.now() + timedelta(hours=24)
    agendamento.status = status
    return agendamento

# TESTS: CRIAR AGENDAMENTO
def test_criar_agendamento_sucesso():
    """Deve criar um agendamento quando todos os dados são válidos"""
    db = MagicMock()
    db.query().filter().first.return_value = None

    dados = make_dados()
    resultado = criar_agendamento(db, dados)

    db.add.assert_called_once()
    db.commit.assert_called_once()

def test_criar_agendamento_horario_passado():
    """Deve rejeitar agendamento em horário passado"""
    db = MagicMock()
    dados = make_dados(horas_futuras=-1)

    with pytest.raises(ValueError) as erro:
        criar_agendamento(db, dados)

    assert "já passou" in str(erro.value)

def test_criar_agendamento_horario_duplicado():
    """Deve rejeitar agendamento no mesmo horário com o mesmo barbeiro"""
    db = MagicMock()
    db.query().filter().first.return_value = make_agendamento_fake()

    dados = make_dados()

    with pytest.raises(ValueError) as erro:
        criar_agendamento(db, dados)

    assert "já possui um agendamento" in str(erro.value)

# TESTES: LISTAR AGENDAMENTOS
def test_listar_agendamentos():
    """Deve retornar lista de agendamentos"""
    db = MagicMock()
    db.query().all.return_value = [make_agendamento_fake()]

    resultado = listar_agendamentos(db)

    assert len(resultado) == 1

# TESTES: CANCELAR AGENDAMENTO
def test_cancelar_agendamento_sucesso():
    """Deve cancelar um agendamento confirmado"""
    db = MagicMock()
    agendamento = make_agendamento_fake(status="confirmado")
    db.query().filter().first.return_value = agendamento

    resultado = cancelar_agendamento(db, 1)

    assert agendamento.status == "cancelado"
    db.commit.assert_called_once()

def test_cancelar_agendamento_nao_encontrado():
    """Deve rejeitar cancelamento de agendamento inexistente"""
    db = MagicMock()
    db.query().filter().first.return_value = None

    with pytest.raises(ValueError) as erro:
        cancelar_agendamento(db, 999)

    assert "não encontrado" in str(erro.value)

def test_cancelar_agendamento_ja_cancelado():
    """Deve rejeitar cancelamento de agendamento já cancelado"""
    db = MagicMock()
    agendamento = make_agendamento_fake(status="cancelado")
    db.query().filter().first.return_value = agendamento

    with pytest.raises(ValueError) as erro:
        cancelar_agendamento(db, 1)

    assert "já está cancelado" in str(erro.value)