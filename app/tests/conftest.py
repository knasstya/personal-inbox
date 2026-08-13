import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.db.database import SessionLocal
from app.models import User, Item
from app.services.security import hash_password

@pytest.fixture
def db_session():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
        
@pytest.fixture
def client():
    db = SessionLocal()

    try:
        # Delete dependent records first because Item.user_id
        # references User.id.
        db.query(Item).delete()
        db.query(User).delete()
        db.commit()

        # Create test user using the actual User model fields.
        user = User(
            username="testuser",
            email="testuser@example.com",
            hashed_password=hash_password("testpassword"),
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        yield TestClient(app)

    finally:
        db.close()


@pytest.fixture
def auth_client(client):
    response = client.post(
        "/auth/login",
        json={
            "username": "testuser",
            "password": "testpassword",
        },
    )

    assert response.status_code == 200, response.text

    token = response.json()["access_token"]

    client.headers.update({
        "Authorization": f"Bearer {token}"
    })

    return client

@pytest.fixture
def user_id():
    db = SessionLocal()

    try:
        user = db.query(User).filter(User.username == "testuser").first()

        assert user is not None

        return user.id
    finally:
        db.close()