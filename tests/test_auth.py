from fastapi.testclient import TestClient
from app.main import app
from app.schemas import UserOut
from .testdb import session, client


def test_register_user(client):
    print("Testing user register")
    res = client.post(
        "/auth/register", json={"email": "test123@gmail.com", "password": "password123"}
    )

    new_user = UserOut(**res.json())
    assert new_user.email == "test123@gmail.com"
    assert res.status_code == 201
