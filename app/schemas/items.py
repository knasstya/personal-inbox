from pydantic import BaseModel, ConfigDict


class ItemCreate(BaseModel):
    title: str
    url: str


class ItemUpdate(BaseModel):
    title: str
    url: str


class ItemResponse(BaseModel):
    id: int
    title: str
    url: str
    content: str | None
    summary: str | None
    tags: list[str] | None
    processing_error: str | None
    processing_status: str
    model_config = ConfigDict(from_attributes=True)