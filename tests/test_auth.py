from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_usuario_nao_admin_nao_acessa_rota_admin():
    response = client.post(
        "/auth/token",
        data={
            "username": "dr.joao",
            "password": "senha-medico"
        }
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    response = client.get("/admin/usuarios",headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 403