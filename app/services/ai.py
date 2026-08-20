from google import genai
from google.genai import types

from app.config import settings
from app.schemas.ai import AIAnalysis


client = genai.Client(api_key=settings.gemini_api_key)


def analyze_content(content: str) -> AIAnalysis:
    if not content.strip():
        raise ValueError("Content cannot be empty.")

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=(
            "Analyze the following saved web content for a personal knowledge "
            "inbox. Produce a concise summary and 3 to 5 useful tags. "
            "Tags must be lowercase, concise, and unique. "
            "Tags should describe the main topics, technologies, concepts, "
            "or subject areas. Prefer specific and useful tags over generic ones. "
            "Avoid tags such as 'article', 'guide', 'content', 'technology', "
            "or 'web' unless they are genuinely important to the content. "
            "Use consistent lowercase names for technologies and concepts, "
            "for example 'fastapi' rather than 'FastAPI'.\n\n"
            f"CONTENT:\n{content}"
        ),
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=AIAnalysis,
        ),
    )

    if response.parsed is None:
        raise ValueError("Gemini returned no structured analysis.")

    return response.parsed