from tests.conftest import auth, login

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