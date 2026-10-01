
import os

os.environ.update({
    "SECRET_KEY": "chave-exclusiva-testes-0123456789",
    "MFA_DEMO_CODE": "123456",
    "LABORATORIO_CLIENT_SECRET": "segredo-m2m-teste",
    "ADMIN_PASSWORD": "senha-admin-teste",
    "DR_JOAO_PASSWORD": "senha-medico-teste",
    "RECEPCAO_PASSWORD": "senha-recepcao-teste",
    "DATABASE_URL": "sqlite:///./banco-nao-utilizado.db",
})

import pytest

from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine
from itertools import count

import app.main as main_module

from app.main import app
from app.database.database import get_db
from app.auth.security import hash_password
from app.models.usuario import Usuario
from app.models.consulta import Consulta


_test_client_ips = count(1)

@pytest.fixture
def test_engine():

    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:

        usuarios = [
            Usuario(
                username="admin",
                senha_hash=hash_password("senha-admin-teste"),
                role="admin",
                mfa_enabled=True,
            ),
            Usuario(
                username="dr.joao",
                senha_hash=hash_password("senha-medico-teste"),
                role="medico",
                mfa_enabled=False,
            ),
            Usuario(
                username="dr.maria",
                senha_hash=hash_password("senha-medico2-teste"),
                role="medico",
                mfa_enabled=False,
            ),
            Usuario(
                username="recepcao",
                senha_hash=hash_password("senha-recepcao-teste"),
                role="recepcionista",
                mfa_enabled=False,
            ),
        ]

        session.add_all(usuarios)
        session.flush()

        consultas = [
            Consulta(
                id=1,
                paciente="Paciente Joao",
                especialidade="Cardiologia",
                observacao_interna="Informacao interna teste",
                owner_username="dr.joao",
            ),
            Consulta(
                id=2,
                paciente="Paciente Maria",
                especialidade="Dermatologia",
                observacao_interna="Informacao confidencial teste",
                owner_username="dr.maria",
            ),
        ]

        session.add_all(consultas)
        session.commit()

    yield engine

    engine.dispose()


@pytest.fixture
def db_session(test_engine):

    with Session(test_engine) as session:
        yield session


@pytest.fixture
def client(test_engine, monkeypatch):

    monkeypatch.setattr(
        main_module,
        "create_db_and_tables",
        lambda: None,
    )

    monkeypatch.setattr(
        main_module,
        "inicializar_dados",
        lambda: None,
    )

    def override_get_db():

        with Session(test_engine) as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(
        app,
        client=(f"127.0.0.{next(_test_client_ips)}", 50000)
        ) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()


def login(client, username, password, otp=None):

    data = {
        "username": username,
        "password": password,
    }

    if otp:
        data["otp"] = otp

    return client.post("/auth/token", data=data)


def auth(client, username, password, otp=None):

    response = login(client, username, password, otp)

    assert response.status_code == 200, response.text

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }