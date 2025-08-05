from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from app.main import app
from app.config import settings
from app.database import get_session, Base


TEST_DB_URL = f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}_test"

if TEST_DB_URL:
    engine = create_engine(TEST_DB_URL)
else:
    raise Exception({"message": "Test DB URL missing."})

TestSessionLocal = sessionmaker(autoflush=False, bind=engine)


@pytest.fixture()
def session():
    print("Create test session")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    print("Create test client")

    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_session] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    print("Create test user")
    user_data = {"email": "test123@gmail.com", "password": "password123"}
    res = client.post("/auth/register/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user
