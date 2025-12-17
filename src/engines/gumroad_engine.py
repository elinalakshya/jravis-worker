import os
import requests

GUMROAD_API_KEY = os.getenv("GUMROAD_API_KEY")

def publish_to_gumroad(title: str, file_url: str, price_usd: int = 9):
    if not GUMROAD_API_KEY:
        raise RuntimeError("GUMROAD_API_KEY missing")

    url = "https://api.gumroad.com/v2/products"

    headers = {
        "Authorization": f"Bearer {GUMROAD_API_KEY}"
    }

    data = {
        "name": title,
        "price": price_usd * 100,  # cents
        "description": (
            f"{title}\n\n"
            f"Instant download via secure link:\n{file_url}\n\n"
            "Auto-published by JRAVIS"
        ),
        "published": True,
        "external_url": file_url
    }

    r = requests.post(url, headers=headers, data=data, timeout=60)

    if r.status_code != 200:
        raise RuntimeError(
            f"Gumroad product create failed "
            f"[{r.status_code}]: {r.text}"
        )

    return r.json()
