
def test_login_bloqueia_excesso_de_requisicoes(client):
    dados = {
        "username": "dr.joao",
        "password": "senha-medico-teste"
    }

    for _ in range(5):
        response = client.post(
            "/auth/token",
            data=dados
        )

        assert response.status_code == 200

    response = client.post(
        "/auth/token",
        data=dados
    )

    assert response.status_code == 429