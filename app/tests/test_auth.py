def test_register(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "registeruser",
            "email": "register@example.com",
            "password": "secret123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "registeruser"
    assert data["email"] == "register@example.com"
    assert "password" not in data
    assert "hashed_password" not in data


def test_register_duplicate_username(client):
    payload = {
        "username": "duplicateuser",
        "email": "first@example.com",
        "password": "secret123",
    }

    first_response = client.post(
        "/auth/register",
        json=payload,
    )

    assert first_response.status_code == 200

    second_response = client.post(
        "/auth/register",
        json={
            "username": "duplicateuser",
            "email": "second@example.com",
            "password": "secret123",
        },
    )

    assert second_response.status_code == 400


def test_login(client):
    response = client.post(
        "/auth/login",
        json={
            "username": "testuser",
            "password": "testpassword",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)


def test_login_wrong_password(client):
    response = client.post(
        "/auth/login",
        json={
            "username": "testuser",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401