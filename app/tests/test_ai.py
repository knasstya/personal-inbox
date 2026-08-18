from app.schemas.ai import AIAnalysis
from app.services.ai import analyze_content


def test_analyze_content(monkeypatch):
    class FakeResponse:
        parsed = AIAnalysis(
            summary="FastAPI is a Python framework for building APIs.",
            tags=["python", "fastapi", "web-development"],
        )

    def fake_generate_content(**kwargs):
        assert kwargs["model"] == "gemini-3.6-flash"
        assert "FastAPI" in kwargs["contents"]

        return FakeResponse()

    monkeypatch.setattr(
        "app.services.ai.client.models.generate_content",
        fake_generate_content,
    )

    result = analyze_content(
        "FastAPI is a Python web framework for building APIs."
    )

    assert isinstance(result, AIAnalysis)
    assert result.summary == (
        "FastAPI is a Python framework for building APIs."
    )
    assert result.tags == [
        "python",
        "fastapi",
        "web-development",
    ]


def test_analyze_content_empty():
    try:
        analyze_content("")
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert str(exc) == "Content cannot be empty."

def test_analyze_content_no_structured_analysis(monkeypatch):
    class FakeResponse:
        parsed = None

    def fake_generate_content(**kwargs):
        return FakeResponse()

    monkeypatch.setattr(
        "app.services.ai.client.models.generate_content",
        fake_generate_content,
    )

    try:
        analyze_content("Some valid content.")
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert str(exc) == "Gemini returned no structured analysis."