import pytest
from backend.app.services.auth_service import criar_token
from backend.app.services.seguranca import usuario_atual
from unittest.mock import MagicMock
from fastapi import HTTPException

def test_usuario_atual_sucesso():
    token = criar_token("teste@email.com")

    usuario_fake = MagicMock()
    usuario_fake.email = "teste@email.com"

    db = MagicMock()
    db.query().filter().first.return_value = usuario_fake

    resultado = usuario_atual(token, db)

    assert resultado.email == "teste@email.com"

def test_usuario_atual_token_invalido():
    db = MagicMock()
    with pytest.raises(HTTPException) as erro:
        usuario_atual("token", db)

        assert erro.value.status_code == 401