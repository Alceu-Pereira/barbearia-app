import pytest
from unittest.mock import MagicMock
from backend.app.services.barbeiro_service import (
    criar_barbeiro,
    listar_barbeiros,
    buscar_barbeiro,
    atualizar_barbeiro,
    deletar_barbeiro
)
from backend.app.schemas.barbeiro import BarbeiroCreate, BarbeiroUpdate

def make_barbeiro_fake(id=1, nome="João Silva", especialidade="Corte", ativo=True):
    barbeiro = MagicMock()
    barbeiro.id = id
    barbeiro.nome = nome
    barbeiro.especialidade = especialidade
    barbeiro.ativo = ativo
    return barbeiro

# ------- TESTES: CRIAR BARBEIRO ---------------------------------
def test_criar_barbeiro_sucesso():
    db = MagicMock()
    db.query().filter().first.return_value = None

    dados = BarbeiroCreate(nome="Pedro Santos", especialidade="Masculino")
    resultado = criar_barbeiro(db, dados)

    db.add.assert_called_once()
    db.commit.assert_called_once()

def test_criar_barbeiro_nome_duplicado():
    db = MagicMock()
    db.query().filter().first.return_value = make_barbeiro_fake()

    dados = BarbeiroCreate(nome="João Silva", especialidade="Corte")

    with pytest.raises(ValueError) as erro:
        criar_barbeiro(db, dados)

    assert "Já existe um barbeiro com esse nome." in str(erro.value)

# ------ TESTES: LISTAR BARBEIROS ----------------------------------
def test_listar_barbeiros():
    db = MagicMock()
    db.query().filter().all.return_value = [make_barbeiro_fake()]

    resultado = listar_barbeiros(db)

    assert len(resultado) == 1

# ------- TESTES: BUSCAR BARBEIRO -----------------------------------
def test_buscar_barbeiro_sucesso():
    db = MagicMock()
    db.query().filter().first.return_value = make_barbeiro_fake()

    resultado = buscar_barbeiro(db, 1)

    assert resultado.nome == "João Silva"

def test_buscar_barbeiro_nao_encontrado():
    db = MagicMock()
    db.query().filter().first.return_value = None

    with pytest.raises(ValueError) as erro:
        buscar_barbeiro(db, 999)

    assert "não encontrado" in str(erro.value)

# ─── TESTES: ATUALIZAR BARBEIRO ─────────────────────────
def test_atualizar_barbeiro_sucesso():
    db = MagicMock()
    barbeiro = make_barbeiro_fake()
    db.query().filter().first.return_value = barbeiro

    dados = BarbeiroUpdate(nome="João Atualizado")
    resultado = atualizar_barbeiro(db, 1, dados)

    assert barbeiro.nome == "João Atualizado"
    db.commit.assert_called_once()


def test_atualizar_barbeiro_nao_encontrado():
    db = MagicMock()
    db.query().filter().first.return_value = None

    dados = BarbeiroUpdate(nome="Novo Nome")

    with pytest.raises(ValueError):
        atualizar_barbeiro(db, 999, dados)


# ─── TESTES: DELETAR BARBEIRO ────────────────────────────
def test_deletar_barbeiro_sucesso():
    db = MagicMock()
    barbeiro = make_barbeiro_fake()
    db.query().filter().first.return_value = barbeiro

    resultado = deletar_barbeiro(db, 1)

    db.delete.assert_called_once_with(barbeiro)
    db.commit.assert_called_once()


def test_deletar_barbeiro_nao_encontrado():
    db = MagicMock()
    db.query().filter().first.return_value = None

    with pytest.raises(ValueError):
        deletar_barbeiro(db, 999)