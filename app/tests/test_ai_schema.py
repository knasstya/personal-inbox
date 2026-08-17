from app.schemas.ai import AIAnalysis


def test_ai_analysis_schema():
    analysis = AIAnalysis(
        summary="FastAPI is a Python framework for building APIs.",
        tags=["python", "fastapi", "web-development"],
    )

    assert analysis.summary == "FastAPI is a Python framework for building APIs."
    assert analysis.tags == ["python", "fastapi", "web-development"]