from tests.conftest import auth, login
from datetime import timedelta
from app.auth.security import create_access_token

def test_nao_admin_nao_acessa_rota_admin(client):
    headers = auth(client, "dr.joao", "senha2")
    assert client.get("/admin/usuarios", headers=headers).status_code == 403

def test_admin_acessa_rota_admin_com_mfa(client):
    headers = auth(client, "admin", "senha1", otp="123456")
    resp = client.get("/admin/usuarios", headers=headers)
    assert resp.status_code == 200
    assert "senha_hash" not in resp.json()[0]

def test_admin_sem_mfa_e_recusado(client):
    assert login(client, "admin", "senha1").status_code == 401

def test_token_expirado_e_rejeitado(client):
    token = create_access_token("dr.joao", "medico", expires_delta=timedelta(seconds=-1))
    r = client.get("/consultas/", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 401