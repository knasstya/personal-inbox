from app.services.items import process_item_content


def test_get_items(auth_client):
    response = auth_client.get("/items/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_item(auth_client):
    response = auth_client.post(
        "/items/",
        json={
            "title": "Test Item",
            "url": "https://example.com",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Test Item"
    assert data["url"] == "https://example.com"


def test_get_item(auth_client):
    create_response = auth_client.post(
        "/items/",
        json={
            "title": "Single Item",
            "url": "https://example.com",
        },
    )

    assert create_response.status_code == 200

    item_id = create_response.json()["id"]

    response = auth_client.get(f"/items/{item_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == item_id
    assert data["title"] == "Single Item"
    assert data["url"] == "https://example.com"


def test_delete_item(auth_client):
    create_response = auth_client.post(
        "/items/",
        json={
            "title": "Item To Delete",
            "url": "https://example.com",
        },
    )

    assert create_response.status_code == 200

    item_id = create_response.json()["id"]

    response = auth_client.delete(f"/items/{item_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == item_id
    assert data["title"] == "Item To Delete"
    assert data["url"] == "https://example.com"

    get_response = auth_client.get(f"/items/{item_id}")

    assert get_response.status_code == 404


def test_update_item(auth_client):
    create_response = auth_client.post(
        "/items/",
        json={
            "title": "Original Title",
            "url": "https://example.com",
        },
    )

    assert create_response.status_code == 200

    item_id = create_response.json()["id"]

    response = auth_client.put(
        f"/items/{item_id}",
        json={
            "title": "Updated Title",
            "url": "https://updated-example.com",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == item_id
    assert data["title"] == "Updated Title"
    assert data["url"] == "https://updated-example.com"


def test_process_item(auth_client):
    create_response = auth_client.post(
        "/items/",
        json={
            "title": "Process Test",
            "url": "https://example.com",
        },
    )

    assert create_response.status_code == 200

    item_id = create_response.json()["id"]

    response = auth_client.post(f"/items/{item_id}/process")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == item_id
    assert data["title"] == "Process Test"
    assert data["url"] == "https://example.com"


def test_get_item_not_found(auth_client):
    response = auth_client.get("/items/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


def test_delete_item_not_found(auth_client):
    response = auth_client.delete("/items/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


def test_update_item_not_found(auth_client):
    response = auth_client.put(
        "/items/999999",
        json={
            "title": "Does Not Exist",
            "url": "https://example.com",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


def test_process_item_not_found(auth_client):
    response = auth_client.post("/items/999999/process")

    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


def test_process_item_content_success(auth_client, user_id, monkeypatch):
    create_response = auth_client.post(
        "/items/",
        json={
            "title": "Content Test",
            "url": "https://example.com",
        },
    )

    assert create_response.status_code == 200

    item_id = create_response.json()["id"]

    def fake_fetch_and_extract(url):
        return "Extracted test content"

    monkeypatch.setattr(
        "app.services.items.fetch_and_extract",
        fake_fetch_and_extract,
    )

    process_item_content(item_id, user_id)

    response = auth_client.get(f"/items/{item_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["content"] == "Extracted test content"
    assert data["processing_error"] is None


def test_process_item_content_failure(auth_client, user_id, monkeypatch):
    create_response = auth_client.post(
        "/items/",
        json={
            "title": "Failure Test",
            "url": "https://example.com",
        },
    )

    assert create_response.status_code == 200

    item_id = create_response.json()["id"]

    def fake_fetch_and_extract(url):
        raise Exception("Test processing error")

    monkeypatch.setattr(
        "app.services.items.fetch_and_extract",
        fake_fetch_and_extract,
    )

    process_item_content(item_id, user_id)

    response = auth_client.get(f"/items/{item_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["processing_error"] == "Test processing error"


def test_get_items_requires_auth(client):
    response = client.get("/items/")

    assert response.status_code == 401