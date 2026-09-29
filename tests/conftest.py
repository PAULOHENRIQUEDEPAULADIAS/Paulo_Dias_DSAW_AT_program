import os

os.environ.setdefault("SECRET_KEY", "chave-somente-para-testes-0123456789")

import pytest
from fastapi.testclient import TestClient
from app.main import app



@pytest.fixture
def client():
    return TestClient(app)

def login(client, username, password, otp=None):
    data = {"username": username, "password": password}
    if otp:
        data["otp"] = otp
    return client.post("/auth/token", data=data)

def auth(client, username, password, otp=None):
    token = login(client, username, password, otp).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}