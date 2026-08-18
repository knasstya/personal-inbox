from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    HttpUrl,
    TypeAdapter,
    field_validator,
)


http_url_adapter = TypeAdapter(HttpUrl)


class ItemCreate(BaseModel):
    title: str = Field(min_length=1)
    url: str

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        http_url_adapter.validate_python(value)
        return value


class ItemUpdate(BaseModel):
    title: str = Field(min_length=1)
    url: str

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        http_url_adapter.validate_python(value)
        return value


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