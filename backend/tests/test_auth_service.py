from jose import jwt
from backend.app.services.auth_service import (
    criar_token,
    autenticar_usuario,
    SECRET_KEY,
    ALGORITHM
)
from unittest.mock import MagicMock
from backend.app.services.auth_service import gerar_hash_senha

def test_criar_token():
    email = "alceu@email.com"

    token = criar_token(email)

    assert token is not None

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert payload["sub"] == email

def test_autenticar_usuario_sucesso():
    usuario_fake = MagicMock()
    usuario_fake.email = "alceu@email.com"
    usuario_fake.senha_hash = gerar_hash_senha("senha123")

    db = MagicMock()
    db.query().filter().first.return_value = usuario_fake

    resultado = autenticar_usuario(db, "alceu@email.com", "senha123")

    assert resultado is not None
    assert resultado.email == "alceu@email.com"

def test_autenticar_usuario_senha_incorreta():
    usuario_fake = MagicMock()
    usuario_fake.email = "alceu@email.com"
    usuario_fake.senha_hash = gerar_hash_senha("senha123")

    db = MagicMock()
    db.query().filter().first.return_value = usuario_fake

    resultado = autenticar_usuario(db, "alceu@email.com", "senhaerrada")

    assert resultado is None

def test_autenticar_usuario_email_nao_encontrado():
    db = MagicMock()
    db.query().filter().first.return_value = None

    resultado = autenticar_usuario(db, "naoexiste@email.com", "qualquersenha")

    assert resultado is None