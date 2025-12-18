import os
import requests

GUMROAD_API_KEY = os.getenv("GUMROAD_API_KEY")
GUMROAD_PRODUCT_ID = os.getenv("GUMROAD_PRODUCT_ID")

if not GUMROAD_API_KEY:
    raise RuntimeError("❌ GUMROAD_API_KEY missing")

if not GUMROAD_PRODUCT_ID:
    raise RuntimeError("❌ GUMROAD_PRODUCT_ID missing")


def update_gumroad_content_url(content_url: str):
    """
    Updates content_url of an existing Gumroad product.
    NO uploads. NO product creation.
    """

    url = f"https://api.gumroad.com/v2/products/{GUMROAD_PRODUCT_ID}"

    payload = {
        "access_token": GUMROAD_API_KEY,
        "content_url": content_url
    }

    print("🛒 Updating Gumroad product")
    print(f"📦 PRODUCT ID = {GUMROAD_PRODUCT_ID}")
    print(f"🔁 Setting content_url = {content_url}")

    response = requests.put(url, data=payload, timeout=30)

    if response.status_code != 200:
        raise RuntimeError(
            f"Gumroad update failed: {response.status_code} {response.text}"
        )

    print("✅ Gumroad content_url updated successfully")

    return {
        "status": "success",
        "content_url": content_url
    }
