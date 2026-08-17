from google import genai
from google.genai import types

from app.config import settings
from app.schemas.ai import AIAnalysis


client = genai.Client(api_key=settings.gemini_api_key)


def analyze_content(content: str) -> AIAnalysis:
    if not content.strip():
        raise ValueError("Content cannot be empty.")

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=(
            "Analyze the following saved web content for a personal knowledge "
            "inbox. Produce a concise summary and a small set of useful tags. "
            "Tags should describe the main topics, technologies, concepts, "
            "or subject areas. Avoid overly generic tags.\n\n"
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