from pydantic import BaseModel


class AIAnalysis(BaseModel):
    summary: str
    tags: list[str]