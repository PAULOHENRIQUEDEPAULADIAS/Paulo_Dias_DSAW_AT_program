# tests/test_consulta.py
from tests.conftest import auth

def test_listar_consultas_autenticado(client):
    headers = auth(client, "dr.joao", "senha2")
    dados = client.get("/consultas/", headers=headers).json()
    assert len(dados) > 0
    assert "observacao_interna" not in dados[0]

def test_sem_token_retorna_401(client):
    assert client.get("/consultas/").status_code == 401

def test_ownership_bloqueia_consulta_de_outro(client):
    headers = auth(client, "dr.joao", "senha2")
    assert client.get("/consultas/2", headers=headers).status_code == 403

def test_recepcionista_nao_cria_consulta(client):
    headers = auth(client, "recepcao", "senha3")
    r = client.post("/consultas/", json={"paciente": "X", "especialidade": "Y"}, headers=headers)
    assert r.status_code == 403

def test_medico_cria_consulta_propria(client):
    headers = auth(client, "dr.joao", "senha2")
    r = client.post("/consultas/", json={"paciente": "Ana", "especialidade": "Ortopedia"}, headers=headers)
    assert r.status_code == 201