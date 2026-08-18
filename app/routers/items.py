from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends

from app.schemas.items import ItemCreate, ItemUpdate, ItemResponse
from app.services.items import (
    create_item as create_item_service,
    get_items as get_items_service,
    search_items as search_items_service,
    get_item as get_item_service,
    delete_item as delete_item_service,
    update_item as update_item_service,
    process_item_content,
)
from app.dependencies import get_current_user_id


router = APIRouter()


@router.get("/", response_model=list[ItemResponse])
def get_items(
    q: str | None = None,
    user_id: int = Depends(get_current_user_id),
):
    if q:
        return search_items_service(
            query=q,
            user_id=user_id,
        )

    return get_items_service(user_id)


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(
    item_id: int,
    user_id: int = Depends(get_current_user_id),
):
    item = get_item_service(item_id, user_id)

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return item


@router.delete("/{item_id}", response_model=ItemResponse)
def delete_item(
    item_id: int,
    user_id: int = Depends(get_current_user_id),
):
    deleted_item = delete_item_service(item_id, user_id)

    if deleted_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return deleted_item


@router.post("/", response_model=ItemResponse)
def create_item(
    item: ItemCreate,
    background_tasks: BackgroundTasks,
    user_id: int = Depends(get_current_user_id),
):
    created_item = create_item_service(
        item.title,
        item.url,
        user_id,
    )

    background_tasks.add_task(
        process_item_content,
        created_item.id,
        user_id,
    )

    return created_item


@router.post("/{item_id}/process", response_model=ItemResponse)
def process_item(
    item_id: int,
    background_tasks: BackgroundTasks,
    user_id: int = Depends(get_current_user_id),
):
    item = get_item_service(item_id, user_id)

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    background_tasks.add_task(
        process_item_content,
        item.id,
        user_id,
    )

    return item


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: int,
    item: ItemUpdate,
    user_id: int = Depends(get_current_user_id),
):
    updated_item = update_item_service(
        item_id,
        item.title,
        item.url,
        user_id,
    )

    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return updated_item