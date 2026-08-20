from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = (
        "postgresql://postgres:postgres@127.0.0.1:5433/personal_inbox"
    )

    jwt_secret: str = "dev-only-change-this-secret"
    access_token_expire_minutes: int = 30

    auto_create_tables: bool = True

    gemini_api_key: str | None = None
    gemini_model: str = "gemini-3.6-flash"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()