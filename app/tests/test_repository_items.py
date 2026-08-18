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

def test_filter_items_by_tag(db_session, client, user_id):
    tagged_item = Item(
        title="FastAPI Guide",
        url="https://example.com/fastapi",
        summary="A guide to FastAPI",
        content="FastAPI provides tools for creating web APIs.",
        tags=["python", "fastapi"],
        user_id=user_id,
    )

    other_item = Item(
        title="Cooking Guide",
        url="https://example.com/cooking",
        summary="A guide to cooking",
        content="Cooking recipes and techniques.",
        tags=["cooking", "food"],
        user_id=user_id,
    )

    db_session.add_all([tagged_item, other_item])
    db_session.commit()

    results = search_items(
        db_session,
        user_id=user_id,
        tag="fastapi",
    )

    assert len(results) == 1
    assert results[0].title == "FastAPI Guide"


def test_filter_items_by_tag_does_not_match_different_tag(
    db_session,
    client,
    user_id,
):
    item = Item(
        title="Python Guide",
        url="https://example.com/python",
        summary="A guide to Python",
        content="Python programming.",
        tags=["python"],
        user_id=user_id,
    )

    db_session.add(item)
    db_session.commit()

    results = search_items(
        db_session,
        user_id=user_id,
        tag="fastapi",
    )

    assert results == []


def test_filter_items_by_tag_only_returns_current_users_items(
    db_session,
    client,
    user_id,
):
    other_user = User(
        username="othertaguser",
        email="othertag@example.com",
        hashed_password=hash_password("otherpassword"),
    )

    db_session.add(other_user)
    db_session.commit()
    db_session.refresh(other_user)

    own_item = Item(
        title="My FastAPI Resource",
        url="https://example.com/my-fastapi",
        tags=["fastapi"],
        user_id=user_id,
    )

    other_item = Item(
        title="Other FastAPI Resource",
        url="https://example.com/other-fastapi",
        tags=["fastapi"],
        user_id=other_user.id,
    )

    db_session.add_all([own_item, other_item])
    db_session.commit()

    results = search_items(
        db_session,
        user_id=user_id,
        tag="fastapi",
    )

    assert len(results) == 1
    assert results[0].title == "My FastAPI Resource"
    assert results[0].user_id == user_id

def test_search_items_by_query_and_tag(db_session, client, user_id):
    matching_item = Item(
        title="FastAPI Authentication",
        url="https://example.com/fastapi-auth",
        summary="Authentication with FastAPI",
        content="FastAPI authentication using JWT.",
        tags=["python", "fastapi", "authentication"],
        user_id=user_id,
    )

    wrong_tag_item = Item(
        title="FastAPI Database Guide",
        url="https://example.com/fastapi-db",
        summary="Working with databases in FastAPI",
        content="FastAPI with PostgreSQL.",
        tags=["python", "fastapi", "database"],
        user_id=user_id,
    )

    wrong_query_item = Item(
        title="Authentication in Django",
        url="https://example.com/django-auth",
        summary="Authentication with Django",
        content="Django authentication using sessions.",
        tags=["python", "django", "authentication"],
        user_id=user_id,
    )

    db_session.add_all(
        [
            matching_item,
            wrong_tag_item,
            wrong_query_item,
        ]
    )
    db_session.commit()

    results = search_items(
        db_session,
        user_id=user_id,
        query="authentication",
        tag="fastapi",
    )

    assert len(results) == 1
    assert results[0].title == "FastAPI Authentication"


def test_search_items_by_query_and_tag_only_returns_current_users_items(
    db_session,
    client,
    user_id,
):
    other_user = User(
        username="othersearchuser",
        email="othersearch@example.com",
        hashed_password=hash_password("otherpassword"),
    )

    db_session.add(other_user)
    db_session.commit()
    db_session.refresh(other_user)

    own_item = Item(
        title="My FastAPI Authentication",
        url="https://example.com/my-auth",
        summary="Authentication with FastAPI",
        content="FastAPI authentication.",
        tags=["fastapi", "authentication"],
        user_id=user_id,
    )

    other_item = Item(
        title="Other FastAPI Authentication",
        url="https://example.com/other-auth",
        summary="Authentication with FastAPI",
        content="FastAPI authentication.",
        tags=["fastapi", "authentication"],
        user_id=other_user.id,
    )

    db_session.add_all([own_item, other_item])
    db_session.commit()

    results = search_items(
        db_session,
        user_id=user_id,
        query="authentication",
        tag="fastapi",
    )

    assert len(results) == 1
    assert results[0].title == "My FastAPI Authentication"