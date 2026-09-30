from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_laboratorio_obtem_token():
    response = client.post(
        "/auth/token/m2m",
        data={
            "client_id": "laboratorio_xyz",
            "client_secret": "segredo-laboratorio",
            "scope": "consultas:leitura",
        }
    )

    assert response.status_code == 200

    dados = response.json()

    assert "access_token" in dados
    assert dados["token_type"] == "bearer"
    assert dados["scope"] == "consultas:leitura"


def test_laboratorio_nao_pode_solicitar_escopo_de_escrita():
    response = client.post(
        "/auth/token/m2m",
        data={
            "client_id": "laboratorio_xyz",
            "client_secret": "segredo-laboratorio",
            "scope": "consultas:escrita",
        }
    )

    assert response.status_code == 403

def test_laboratorio_acessa_consultas_com_scope():
    response = client.post(
        "/auth/token/m2m",
        data={
            "client_id": "laboratorio_xyz",
            "client_secret": "segredo-laboratorio",
            "scope": "consultas:leitura",
        }
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    response = client.get(
        "/laboratorio/consultas",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

def test_token_de_usuario_nao_pode_ser_usado_como_token_m2m():
    response = client.post(
        "/auth/token",
        data={
            "username": "dr.joao",
            "password": "senha2",
        }
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    response = client.get(
        "/laboratorio/consultas",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 401