def test_resposta_contem_cabecalhos_de_seguranca(client):
    response = client.get("/docs")

    assert response.headers.get("X-Frame-Options") == "DENY"
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert response.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"
    assert response.headers.get("Permissions-Policy") == (
        "camera=(), microphone=(), geolocation=()"
    )
    assert response.headers.get("Cache-Control") == "no-store"

    assert "Strict-Transport-Security" not in response.headers
    assert response.headers.get("Cache-Control") == "no-store"
