from app.schemas.users import UserCreate, UserResponse


def test_user_create_schema():
    user = UserCreate(
        username="nasta",
        email="nasta@example.com",
        password="secret123",
    )

    assert user.username == "nasta"
    assert user.email == "nasta@example.com"
    assert user.password == "secret123"


def test_user_response_schema_does_not_expose_password():
    user = UserResponse(
        id=1,
        username="nasta",
        email="nasta@example.com",
    )

    data = user.model_dump()

    assert data["username"] == "nasta"
    assert data["email"] == "nasta@example.com"
    assert "password" not in data
    assert "hashed_password" not in data