import os
import requests

GUMROAD_API_KEY = os.getenv("GUMROAD_API_KEY")
GUMROAD_API_BASE = "https://api.gumroad.com/v2"

def update_gumroad_content_url(product_id: str, content_url: str):
    """
    Updates an existing Gumroad product to point to a new content_url
    """

    if not GUMROAD_API_KEY:
        raise Exception("GUMROAD_API_KEY missing")

    url = f"{GUMROAD_API_BASE}/products/{product_id}"
    payload = {
        "access_token": GUMROAD_API_KEY,
        "content_url": content_url
    }

    response = requests.put(url, data=payload, timeout=30)

    if response.status_code != 200:
        raise Exception(f"Gumroad API error: {response.text}")

    data = response.json()

    if not data.get("success"):
        raise Exception(f"Gumroad update failed: {data}")

    print("✅ Gumroad product updated successfully")
    return data
