def update_gumroad_content_url(product_id: str, content_url: str):
    import os
    import requests

    api_key = os.getenv("GUMROAD_API_KEY")
    if not api_key:
        raise RuntimeError("❌ GUMROAD_API_KEY missing")

    url = f"https://api.gumroad.com/v2/products/{product_id}"
    headers = {"Authorization": f"Bearer {api_key}"}

    data = {
        "product[content_url]": content_url
    }

    print("🛒 Updating Gumroad product content_url")

    r = requests.put(url, headers=headers, data=data, timeout=30)

    if not r.ok:
        raise RuntimeError(f"Gumroad update failed: {r.text}")

    print("✅ Gumroad content_url updated successfully")
    return r.json()
