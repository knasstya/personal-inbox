from app.db.database import SessionLocal
from app.models import Item
from app.services.content import fetch_and_extract
from app.services.ai import analyze_content
from app.repositories.items import search_items as search_items_repository

def process_item_content(item_id: int, user_id: int):
    db = SessionLocal()

    try:
        item = (
            db.query(Item)
            .filter(
                Item.id == item_id,
                Item.user_id == user_id,
            )
            .first()
        )

        if item is None:
            return None

        item.processing_status = "processing"
        item.processing_error = None

        db.commit()
        db.refresh(item)

        try:
            content = fetch_and_extract(item.url)

            item.content = content
            item.summary = None
            item.tags = None

            try:
                analysis = analyze_content(content)

                item.summary = analysis.summary
                item.tags = analysis.tags
                item.processing_status = "completed"

            except Exception as e:
                item.processing_status = "failed"
                item.processing_error = str(e)

        except Exception as e:
            item.processing_status = "failed"
            item.processing_error = str(e)

        db.commit()
        db.refresh(item)

        return item

    finally:
        db.close()


def create_item(title: str, url: str, user_id: int):
    db = SessionLocal()

    try:
        item = Item(
            title=title,
            url=url,
            user_id=user_id,
        )

        db.add(item)
        db.commit()
        db.refresh(item)

        return item

    finally:
        db.close()


def get_items(user_id: int):
    db = SessionLocal()

    try:
        return (
            db.query(Item)
            .filter(Item.user_id == user_id)
            .all()
        )

    finally:
        db.close()


def search_items(
    user_id: int,
    query: str | None = None,
    tag: str | None = None,
):
    db = SessionLocal()

    try:
        return search_items_repository(
            db=db,
            user_id=user_id,
            query=query,
            tag=tag,
        )
    finally:
        db.close()


def get_item(item_id: int, user_id: int):
    db = SessionLocal()

    try:
        return (
            db.query(Item)
            .filter(
                Item.id == item_id,
                Item.user_id == user_id,
            )
            .first()
        )

    finally:
        db.close()


def delete_item(item_id: int, user_id: int):
    db = SessionLocal()

    try:
        item = (
            db.query(Item)
            .filter(
                Item.id == item_id,
                Item.user_id == user_id,
            )
            .first()
        )

        if item is None:
            return None

        db.delete(item)
        db.commit()

        return item

    finally:
        db.close()


def update_item(
    item_id: int,
    title: str,
    url: str,
    user_id: int,
):
    db = SessionLocal()

    try:
        item = (
            db.query(Item)
            .filter(
                Item.id == item_id,
                Item.user_id == user_id,
            )
            .first()
        )

        if item is None:
            return None

        item.title = title
        item.url = url

        db.commit()
        db.refresh(item)

        return item

    finally:
        db.close()