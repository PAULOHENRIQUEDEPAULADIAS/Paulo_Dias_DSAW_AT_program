from tests.conftest import auth


def test_listar_consultas_autenticado(client):
    headers = auth(client, "dr.joao", "senha-medico-teste")

    response = client.get("/consultas/", headers=headers)

    assert response.status_code == 200
    assert len(response.json()) > 0
    assert "observacao_interna" not in response.text


def test_sem_token_retorna_401(client):
    response = client.get("/consultas/")

    assert response.status_code == 401


def test_medico_acessa_sua_propria_consulta(client):
    headers = auth(client, "dr.joao", "senha-medico-teste")

    response = client.get("/consultas/1", headers=headers)

    assert response.status_code == 200


def test_medico_nao_acessa_consulta_de_outro(client):
    headers = auth(client, "dr.joao", "senha-medico-teste")

    response = client.get("/consultas/2", headers=headers)

    assert response.status_code == 403


def test_recepcionista_nao_cria_consulta(client):
    headers = auth(client, "recepcao", "senha-recepcao-teste")

    response = client.post("/consultas/",
        json={
            "paciente": "Ana Silva",
            "especialidade": "Cardiologia"
        },
        headers=headers
    )

    assert response.status_code == 403


def test_medico_cria_consulta_propria(client):
    headers = auth(client, "dr.joao", "senha-medico-teste")

    response = client.post("/consultas/",
        json={
            "paciente": "Ana Silva",
            "especialidade": "Cardiologia"
        },
        headers=headers
    )

    assert response.status_code == 201