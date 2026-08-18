from sqlalchemy import exists, func, or_, select
from sqlalchemy.orm import Session

from app.models import Item

def search_items(
    db: Session,
    user_id: int,
    query: str | None = None,
    tag: str | None = None,
    limit: int = 20,
    offset: int = 0,
) -> list[Item]:
    filters = [
        Item.user_id == user_id,
    ]

    if query:
        search_term = f"%{query}%"

        filters.append(
            or_(
                Item.title.ilike(search_term),
                Item.summary.ilike(search_term),
                Item.content.ilike(search_term),
            )
        )

    if tag:
        tag_values = func.json_array_elements_text(Item.tags).table_valued("value")

        filters.append(
            exists(
                select(1)
                .select_from(tag_values)
                .where(tag_values.c.value == tag)
            )
        )

    return (
        db.query(Item)
        .filter(*filters)
        .order_by(Item.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )