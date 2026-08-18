from app.models import Item, User
from app.repositories.items import search_items
from app.services.security import hash_password


def test_search_items_by_title(db_session, client, user_id):
    item = Item(
        title="FastAPI Guide",
        url="https://example.com/fastapi",
        summary="A guide to building APIs with Python",
        content="FastAPI provides tools for creating web APIs.",
        tags=["python", "fastapi"],
        user_id=user_id,
    )

    db_session.add(item)
    db_session.commit()

    results = search_items(
        db_session,
        user_id=user_id,
        query="fastapi",
    )

    assert len(results) == 1
    assert results[0].title == "FastAPI Guide"


def test_search_items_only_returns_current_users_items(
    db_session,
    client,
    user_id,
):
    other_user = User(
        username="otheruser",
        email="other@example.com",
        hashed_password=hash_password("otherpassword"),
    )

    db_session.add(other_user)
    db_session.commit()
    db_session.refresh(other_user)

    own_item = Item(
        title="My FastAPI Resource",
        url="https://example.com/my-fastapi",
        summary="My resource about FastAPI",
        content="FastAPI content",
        tags=["fastapi"],
        user_id=user_id,
    )

    other_item = Item(
        title="Other FastAPI Resource",
        url="https://example.com/other-fastapi",
        summary="Someone else's FastAPI resource",
        content="FastAPI content",
        tags=["fastapi"],
        user_id=other_user.id,
    )

    db_session.add_all([own_item, other_item])
    db_session.commit()

    results = search_items(
        db_session,
        user_id=user_id,
        query="fastapi",
    )

    assert len(results) == 1
    assert results[0].title == "My FastAPI Resource"
    assert results[0].user_id == user_id