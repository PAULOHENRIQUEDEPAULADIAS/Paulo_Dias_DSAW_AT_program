from tests.conftest import auth


def test_rejeita_paciente_com_nome_muito_curto(client):
    headers = auth(client, "dr.joao", "senha-medico-teste")

    response = client.post("/consultas/",
        json={
            "paciente": "A",
            "especialidade": "Cardiologia"
        },
        headers=headers
    )

    assert response.status_code == 422


def test_rejeita_especialidade_invalida(client):
    headers = auth(client, "dr.joao", "senha-medico-teste")

    response = client.post(
        "/consultas/",
        json={
            "paciente": "Ana Silva",
            "especialidade": "Especialidade Inventada"
        },
        headers=headers
    )

    assert response.status_code == 422


def test_rejeita_campo_extra_na_requisicao(client):
    headers = auth(client, "dr.joao", "senha-medico-teste")

    response = client.post(
        "/consultas/",
        json={
            "paciente": "Ana Silva",
            "especialidade": "Cardiologia",
            "campo_nao_permitido": "valor"
        },
        headers=headers
    )

    assert response.status_code == 422