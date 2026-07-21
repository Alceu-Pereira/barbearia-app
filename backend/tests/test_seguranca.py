import pytest
from backend.app.services.auth_service import criar_token
from backend.app.services.seguranca import verificar_admin, admin_ou_cliente
from unittest.mock import MagicMock
from fastapi import HTTPException

def test_verificar_admin_sucesso():
    token = criar_token("teste@email.com")

    usuario_fake = MagicMock()
    usuario_fake.email = "teste@email.com"

    db = MagicMock()
    db.query().filter().first.return_value = usuario_fake

    resultado = verificar_admin(token, db)

    assert resultado.email == "teste@email.com"

def test_verificar_admin_token_invalido():
    db = MagicMock()
    with pytest.raises(HTTPException) as erro:
        verificar_admin("token", db)

        assert erro.value.status_code == 401


def test_verificar_admin_nao_encontrado():
    token = criar_token("teste@email.com")

    db = MagicMock()
    db.query().filter().first.return_value = None

    with pytest.raises(HTTPException) as erro:
        verificar_admin(token, db)

    assert erro.value.status_code == 401

def test_admin_ou_cliente_encontra_admin():
    token = criar_token("teste@email.com")

    usuario_fake = MagicMock()
    usuario_fake.email = "teste@email.com"

    db = MagicMock()
    db.query().filter().first.return_value = usuario_fake

    resultado = admin_ou_cliente(token, db)

    assert resultado.email == "teste@email.com"

def test_admin_ou_cliente_encontra_cliente():
    token = criar_token("teste@email.com")

    cliente_fake = MagicMock()
    cliente_fake.email = "teste@email.com"

    db = MagicMock()
    db.query().filter().first.side_effect = [None, cliente_fake]

    resultado = admin_ou_cliente(token, db)

    assert resultado.email == "teste@email.com"

def test_admin_ou_cliente_nao_encontrado():
    token = criar_token("teste@email.com")

    db = MagicMock()
    db.query().filter().first.side_effect = [None, None]

    with pytest.raises(HTTPException) as erro:
        admin_ou_cliente(token, db)
    
    assert erro.value.status_code == 401
