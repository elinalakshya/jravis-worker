# ==========================================
# GUMROAD ENGINE – CONTENT URL MODE
# ==========================================

import os
import requests


def update_gumroad_content_url(*, product_id: str, content_url: str):
    """
    Updates the content_url of an existing Gumroad product
    """

    api_key = os.getenv("GUMROAD_API_KEY")
    if not api_key:
        raise RuntimeError("❌ GUMROAD_API_KEY not set")

    if not product_id:
        raise RuntimeError("❌ product_id missing")

    if not content_url:
        raise RuntimeError("❌ content_url missing")

    url = f"https://api.gumroad.com/v2/products/{product_id}"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "product[content_url]": content_url
    }

    print("🛒 Updating Gumroad product content_url")
    print("🆔 Product ID:", product_id)
    print("🔗 New content_url:", content_url)

    r = requests.put(url, headers=headers, data=data, timeout=30)

    if not r.ok:
        raise RuntimeError(f"❌ Gumroad update failed: {r.text}")

    print("✅ Gumroad content_url updated successfully")
    return r.json()
