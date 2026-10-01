from tests.conftest import auth
from app.models.consulta import Consulta


def test_api_nao_expoe_observacao_interna(client):
    headers = auth(
        client,
        "dr.joao",
        "senha-medico-teste"
    )

    response = client.get(
        "/consultas/",
        headers=headers
    )

    assert response.status_code == 200
    assert "observacao_interna" not in response.text
    assert "Informacao interna teste" not in response.text


def test_rejeita_payload_xss(client):
    headers = auth(
        client,
        "dr.joao",
        "senha-medico-teste"
    )

    response = client.post(
        "/consultas/",
        headers=headers,
        json={
            "paciente": "<script>alert('xss')</script>",
            "especialidade": "Cardiologia"
        }
    )

    assert response.status_code == 422


def test_template_escapa_conteudo_html(client, db_session):
    consulta = Consulta(
        paciente='<script>alert("xss")</script>',
        especialidade="Cardiologia",
        observacao_interna="Teste XSS",
        owner_username="dr.joao"
    )

    db_session.add(consulta)
    db_session.commit()

    headers = auth(
        client,
        "dr.joao",
        "senha-medico-teste"
    )

    response = client.get(
        "/consultas/pagina",
        headers=headers
    )

    assert response.status_code == 200
    assert "<script>" not in response.text
    assert "&lt;script&gt;" in response.text


def test_rejeita_payload_sql_injection(client):
    headers = auth(
        client,
        "dr.joao",
        "senha-medico-teste"
    )

    response = client.post(
        "/consultas/",
        headers=headers,
        json={
            "paciente": "' OR '1'='1",
            "especialidade": "Cardiologia"
        }
    )

    assert response.status_code == 422


def test_token_com_assinatura_invalida_e_rejeitado(client):
    response = client.get(
        "/consultas/",
        headers={
            "Authorization": "Bearer token.falso.assinatura"
        }
    )

    assert response.status_code == 401