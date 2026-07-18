import pytest
from unittest.mock import MagicMock
from backend.app.services.cliente_service import (
    registrar_cliente,
    autenticar_cliente,
    criar_cliente,
    listar_clientes,
    buscar_cliente,
    atualizar_cliente,
    deletar_cliente
)
from backend.app.schemas.cliente import ClienteCreate, ClienteUpdate

def make_cliente_fake():
    cliente = MagicMock()
    cliente.id = 1
    cliente.nome = "João"
    cliente.telefone = 99999999
    return cliente


def test_listar_clientes():
    db = MagicMock()
    db.query().all.return_value = [make_cliente_fake()]

    resultado = listar_clientes(db)

    assert len(resultado) == 1


def test_buscar_cliente_sucesso():
    db = MagicMock()
    db.query().filter().first.return_value = make_cliente_fake()

    resultado = buscar_cliente(db, 1)

    assert resultado.nome == "João"



def test_buscar_cliente_nao_encontrado():
    db = MagicMock()
    db.query().filter().first.return_value = None

    with pytest.raises(ValueError) as erro:
        buscar_cliente(db, 999)


    assert "não encontrado" in str(erro.value)


def test_atualizar_cliente_sucesso():
    db = MagicMock()
    cliente = make_cliente_fake()
    db.query().filter().first.return_value = cliente
    dados = ClienteUpdate(nome="João Atualizado")
    resultado = atualizar_cliente(db, 1, dados)

    assert cliente.nome == "João Atualizado"
    db.commit.assert_called_once()