from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_listar_consultas():
    response = client.get("/consultas/")

    assert response.status_code == 200

    dados = response.json()

    assert isinstance(dados, list)
    assert len(dados) > 0
    assert "observacao_interna" not in dados[0]