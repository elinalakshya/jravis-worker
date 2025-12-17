import os
import requests

GUMROAD_API_KEY = os.getenv("GUMROAD_API_KEY")

def publish_to_gumroad(title: str, file_url: str, price_usd: int = 9):
    if not GUMROAD_API_KEY:
        raise RuntimeError("GUMROAD_API_KEY missing")

    url = "https://api.gumroad.com/v2/products"

    headers = {
        "Authorization": f"Bearer {GUMROAD_API_KEY}",
        "User-Agent": "JRAVIS/1.0 (https://gumroad.com)",
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "name": title,
        "price": price_usd * 100,
        "description": f"{title}\n\nDownload:\n{file_url}",
        "published": "true",
        "external_url": file_url
    }

    r = requests.post(url, headers=headers, data=data, timeout=60)

    if r.status_code != 200:
        raise RuntimeError(
            f"Gumroad API blocked request "
            f"[{r.status_code}]: {r.text[:300]}"
        )

    return r.json()
