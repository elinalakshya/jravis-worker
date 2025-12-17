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

    payload = {
        "name": title,
        "price": price_usd * 100,   # cents
        "description": f"Auto-published by JRAVIS\n\nDownload: {file_url}",
        "content": file_url,
        "published": True
    }

    r = requests.post(url, headers=headers, data=payload, timeout=60)
    if r.status_code != 200:
        raise RuntimeError(f"Gumroad error {r.status_code}: {r.text}")

    return r.json()
