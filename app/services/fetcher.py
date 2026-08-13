import httpx


def fetch_url(url: str) -> str:
    response = httpx.get(url, timeout=10)
    response.raise_for_status()

    return response.text