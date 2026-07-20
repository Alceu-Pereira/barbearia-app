import pytest
from unittest.mock import MagicMock
from backend.app.services.cliente_service import (
    registrar_cliente,
    autenticar_cliente,
    criar_cliente,
    listar_clientes,
    buscar_cliente,
    atualizar_cliente,
    deletar_cliente,
    criar_token_cliente,
    ALGORITHM,
    SECRET_KEY
)
from backend.app.services.auth_service import gerar_hash_senha
from jose import jwt
from backend.app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteRegistro

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

def test_atualizar_cliente_sucesso():
    db = MagicMock()
    cliente = make_cliente_fake()
    db.query().filter().first.return_value = cliente
    dados = ClienteUpdate(nome="João Atualizado", telefone="999999999")
    resultado = atualizar_cliente(db, 1, dados)

    assert cliente.nome == "João Atualizado"
    assert cliente.telefone == "999999999"
    db.commit.assert_called_once()

def test_buscar_cliente_nao_encontrado():
    db = MagicMock()
    db.query().filter().first.return_value = None

    with pytest.raises(ValueError) as erro:
        buscar_cliente(db, 999)


    assert "não encontrado" in str(erro.value)

def test_deletar_cliente_sucesso():
    db = MagicMock()
    cliente = make_cliente_fake()
    db.query().filter().first.return_value = cliente

    resultado = deletar_cliente(db, 1)

    db.delete.assert_called_once_with(cliente)
    db.commit.assert_called_once()

def test_criar_cliente_sucesso():
    db = MagicMock()
    db.query().filter().first.return_value = None

    dados = ClienteCreate(
        nome="João Santos", telefone= "999999999"
    )
    resultado = criar_cliente(db, dados)

    db.add.assert_called_once()
    db.commit.assert_called_once()

def test_registrar_cliente_sucesso():
    db = MagicMock()
    db.query().filter().first.return_value = None

    dados = ClienteRegistro(
        nome="Pedro Santos",
        telefone="999999999",
        email="teste@barbearia.com",
        senha="senha123"
    )

    resultado = registrar_cliente(db, dados)

    db.add.assert_called_once()
    db.commit.assert_called_once()

def test_registrar_cliente_email_duplicado():
    db = MagicMock()
    cliente = make_cliente_fake()
    db.query().filter().first.return_value = cliente

    dados = ClienteRegistro(
        nome="João",
        telefone="999999999",
        email="teste@email.com",
        senha="senha123"
    )

    with pytest.raises(ValueError) as erro:
        registrar_cliente(db, dados)

    assert "Este email já está cadastrado." in str(erro.value)

def test_registrar_cliente_telefone_duplicado():
    db = MagicMock()
    cliente = make_cliente_fake()
    db.query().filter().first.side_effect = [None, cliente]

    dados = ClienteRegistro(
        nome="João",
        telefone="999999999",
        email="teste@email.com",
        senha="senha123"
    )

    with pytest.raises(ValueError) as erro:
        registrar_cliente(db, dados)

    assert "Este telefone já está cadastrado." in str(erro.value)

def test_criar_cliente_telefone_duplicado():
    db = MagicMock()
    cliente = make_cliente_fake()
    db.query().filter().first.return_value = cliente

    dados = ClienteCreate(
        nome="João",
        telefone="999999999"
    )

    with pytest.raises(ValueError) as erro:
        criar_cliente(db, dados)

    assert "Já existe um cliente com esse telefone." in str(erro.value)

def test_autenticar_cliente_sucesso():
    cliente_fake = MagicMock()
    cliente_fake.email = "teste@email.com"
    cliente_fake.senha_hash = gerar_hash_senha("senha123")

    db = MagicMock()
    db.query().filter().first.return_value = cliente_fake

    resultado = autenticar_cliente(db, "teste@email.com", "senha123")

    assert resultado is not None
    assert resultado.email == "teste@email.com"

def test_autenticar_cliente_email_nao_encontrado():
    db = MagicMock()
    db.query().filter().first.return_value = None

    resultado = autenticar_cliente(db, "naoexiste@email.com", "qualquer senha")

    assert resultado is None

def test_autenticar_cliente_senha_incorreta():
    cliente_fake = MagicMock()
    cliente_fake.email = "teste@email.com"
    cliente_fake.senha_hash = gerar_hash_senha("senha123")

    db = MagicMock()
    db.query().filter().first.return_value = cliente_fake

    resultado = autenticar_cliente(db, "teste@email.com", "senha errada")

    assert resultado is None

def test_autenticar_cliente_sem_senha_cadastrada():
    cliente_fake = MagicMock()
    cliente_fake.email = "teste@email.com"
    cliente_fake.senha_hash = None

    db = MagicMock()
    db.query().filter().first.return_value = cliente_fake

    resultado = autenticar_cliente(db, "teste@email.com", "senha123")

    assert resultado is None


def test_criar_token_cliente():
    id = 1
    email = "teste@email.com"

    token = criar_token_cliente(id, email)

    assert token is not None

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert payload["sub"] == email
    assert payload["cliente_id"] == id
