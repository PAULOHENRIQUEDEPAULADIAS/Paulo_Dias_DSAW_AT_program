
from tests.conftest import auth, login
from datetime import timedelta

from app.auth.security import create_access_token


def test_admin_acessa_rota_admin_com_mfa(client):
    headers = auth(client,"admin","senha-admin-teste",otp="123456")

    response = client.get("/admin/usuarios", headers=headers)

    assert response.status_code == 200
    assert "senha_hash" not in response.text


def test_medico_nao_acessa_rota_admin(client):
    headers = auth(client, "dr.joao", "senha-medico-teste")

    response = client.get("/admin/usuarios", headers=headers)

    assert response.status_code == 403


def test_admin_sem_mfa_e_recusado(client):
    response = login(client, "admin", "senha-admin-teste")

    assert response.status_code == 401


def test_usuario_sem_token_e_recusado(client):
    response = client.get("/consultas/")

    assert response.status_code == 401


def test_token_expirado_e_rejeitado(client):
    token = create_access_token("dr.joao","medico",expires_delta=timedelta(seconds=-1))

    response = client.get("/consultas/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 401


def test_token_invalido_e_rejeitado(client):
    response = client.get("/consultas/",headers={"Authorization": "Bearer token-invalido"})

    assert response.status_code == 401