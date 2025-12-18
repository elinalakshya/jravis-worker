import os
import requests

GUMROAD_API_KEY = os.getenv("GUMROAD_API_KEY")

if not GUMROAD_API_KEY:
    raise RuntimeError("❌ GUMROAD_API_KEY not set")

API_BASE = "https://api.gumroad.com/v2"


def update_gumroad_content_url(product_id: str, content_url: str):
    """
    Update content_url of an EXISTING Gumroad product
    """

    url = f"{API_BASE}/products/{product_id}"

    headers = {
        "Authorization": f"Bearer {GUMROAD_API_KEY}"
    }

    data = {
        "content_url": content_url
    }

    resp = requests.put(url, headers=headers, data=data, timeout=30)

    if resp.status_code != 200:
        raise RuntimeError(
            f"Gumroad API error [{resp.status_code}]: {resp.text}"
        )

    return resp.json()
