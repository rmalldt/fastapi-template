from fastapi.testclient import TestClient
import jwt
from app.main import app
from app.schemas import Token, UserOut
from app.config import settings
from .testdb import session, client, test_user


def test_register_user(client):
    print("Testing user register")
    res = client.post(
        "/auth/register", json={"email": "test123@gmail.com", "password": "password123"}
    )

    new_user = UserOut(**res.json())
    assert new_user.email == "test123@gmail.com"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post(
        "/auth/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )

    login_res = Token(**res.json())

    payload = jwt.decode(
        login_res.access_token, settings.secret_key, algorithms=[settings.algorithm]
    )

    id = int(payload.get("sub"))
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200
