import os
import requests

GUMROAD_API_KEY = os.getenv("GUMROAD_API_KEY")


def publish_to_gumroad(title: str, description: str, zip_path: str):
    if not GUMROAD_API_KEY:
        print("⚠️ Gumroad API key missing, skipping")
        return {"platform": "gumroad", "status": "skipped"}

    print(f"📦 Publishing to Gumroad → {title}")

    url = "https://api.gumroad.com/v2/products"

    data = {
        "access_token": GUMROAD_API_KEY,
        "name": title,
        "description": description,
        "price": 999,  # cents
        "published": True,
    }

    files = {
        "file": open(zip_path, "rb")
    }

    response = requests.post(url, data=data, files=files, timeout=120)

    if response.status_code not in (200, 201):
        raise RuntimeError(f"Gumroad failed: {response.text}")

    print("✅ Gumroad publish success")
    return {
        "platform": "gumroad",
        "status": "success",
        "response": response.json()
    }
