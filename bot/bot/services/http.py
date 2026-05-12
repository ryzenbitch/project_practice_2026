from __future__ import annotations

import httpx


async def check_url(url: str) -> tuple[bool, str]:
    if not url.startswith(("http://", "https://")):
        return False, "URL должен начинаться с http:// или https://"
    try:
        async with httpx.AsyncClient(timeout=6.0, follow_redirects=True) as client:
            response = await client.get(url)
        ok = 200 <= response.status_code < 400
        return ok, f"HTTP {response.status_code} · {response.url}"
    except httpx.HTTPError as exc:
        return False, exc.__class__.__name__
