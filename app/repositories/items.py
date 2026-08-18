from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models import Item


def search_items(
    db: Session,
    user_id: int,
    query: str,
) -> list[Item]:
    search_term = f"%{query}%"

    return (
        db.query(Item)
        .filter(
            Item.user_id == user_id,
            or_(
                Item.title.ilike(search_term),
                Item.summary.ilike(search_term),
                Item.content.ilike(search_term),
            ),
        )
        .all()
    )