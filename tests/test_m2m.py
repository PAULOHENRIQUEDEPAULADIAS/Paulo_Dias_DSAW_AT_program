from tests.conftest import auth


def test_cliente_m2m_consegue_obter_token(client):
    response = client.post(
        "/auth/token/m2m",
        data={
            "client_id": "laboratorio_xyz",
            "client_secret": "segredo-m2m-teste"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_cliente_m2m_nao_acessa_scope_nao_permitido(client):
    response = client.post(
        "/auth/token/m2m",
        data={
            "client_id": "laboratorio_xyz",
            "client_secret": "segredo-m2m-teste",
            "scope": "consultas:escrita"
        }
    )

    assert response.status_code == 403


def test_cliente_m2m_acessa_rota_com_scope_valido(client):
    token_response = client.post(
        "/auth/token/m2m",
        data={
            "client_id": "laboratorio_xyz",
            "client_secret": "segredo-m2m-teste",
            "scope": "consultas:leitura"
        }
    )

    assert token_response.status_code == 200

    token = token_response.json()["access_token"]

    response = client.get(
        "/laboratorio/consultas",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert "observacao_interna" not in response.text


def test_usuario_comum_nao_acessa_rota_m2m(client):
    headers = auth(client, "dr.joao", "senha-medico-teste")

    response = client.get(
        "/laboratorio/consultas",
        headers=headers
    )

    assert response.status_code == 401


def test_cliente_m2m_com_segredo_invalido(client):
    response = client.post(
        "/auth/token/m2m",
        data={
            "client_id": "laboratorio_xyz",
            "client_secret": "segredo-incorreto",
            "scope": "consultas:leitura"
        }
    )

    assert response.status_code == 401


def test_token_m2m_sem_scope_nao_acessa_consultas(client):
    token_response = client.post(
        "/auth/token/m2m",
        data={
            "client_id": "laboratorio_xyz",
            "client_secret": "segredo-m2m-teste"
        }
    )

    assert token_response.status_code == 200

    token = token_response.json()["access_token"]

    response = client.get(
        "/laboratorio/consultas",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403