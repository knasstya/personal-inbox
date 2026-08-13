import pytest
import httpx
from app.services.content import fetch_and_extract
from app.services.fetcher import fetch_url

def test_fetch_and_extract(monkeypatch):
    def fake_fetch_url(_url):
        return "<html><body><h1>Hello</h1></body></html>"

    def fake_extract_text(html):
        return "Hello"

    monkeypatch.setattr(
        "app.services.content.fetch_url",
        fake_fetch_url,
    )

    monkeypatch.setattr(
        "app.services.content.extract_text",
        fake_extract_text,
    )

    result = fetch_and_extract("https://example.com")

    assert result == "Hello"

def test_fetch_url_success(monkeypatch):
    class FakeResponse:
        text = "Hello from the website"

        def raise_for_status(self):
            pass

    def fake_get(_url, timeout):
        assert timeout == 10
        return FakeResponse()

    monkeypatch.setattr(httpx, "get", fake_get)

    result = fetch_url("https://example.com")

    assert result == "Hello from the website"

def test_fetch_url_failure(monkeypatch):
    def fake_get(_url, timeout):
        response = httpx.Response(404)
        response.request = httpx.Request("GET", _url)
        return response

    monkeypatch.setattr(httpx, "get", fake_get)

    with pytest.raises(httpx.HTTPStatusError):
        fetch_url("https://example.com")