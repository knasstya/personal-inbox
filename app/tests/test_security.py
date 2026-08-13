from app.services.security import hash_password, verify_password
from app.services.users import create_user


def test_hash_password():
    password = "secret123"

    hashed_password = hash_password(password)

    assert hashed_password != password
    assert hashed_password.startswith("$argon2")


def test_verify_password():
    password = "secret123"
    hashed_password = hash_password(password)

    assert verify_password(password, hashed_password) is True
    assert verify_password("wrong-password", hashed_password) is False


def test_create_user(db_session):
    user = create_user(
        username="serviceuser",
        email="service@example.com",
        password="secret123",
    )

    assert user.username == "serviceuser"
    assert user.email == "service@example.com"
    assert user.hashed_password != "secret123"
    assert user.hashed_password.startswith("$argon2")