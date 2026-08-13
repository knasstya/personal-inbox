from app.services.fetcher import fetch_url
from app.services.parser import extract_text


def fetch_and_extract(url: str) -> str:
    html = fetch_url(url)
    return extract_text(html)