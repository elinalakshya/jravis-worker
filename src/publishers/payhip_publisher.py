import os
import requests

PAYHIP_API_KEY = os.getenv("PAYHIP_API_KEY")


def publish_to_payhip(title: str, description: str, zip_path: str):
    if not PAYHIP_API_KEY:
        print("⚠️ Payhip API key missing, skipping")
        return {"platform": "payhip", "status": "skipped"}

    print(f"📦 Publishing to Payhip → {title}")

    url = "https://payhip.com/api/v1/products"

    headers = {
        "Authorization": f"Bearer {PAYHIP_API_KEY}"
    }

    data = {
        "title": title,
        "description": description,
        "price": 9.99,
        "product_type": "digital"
    }

    files = {
        "file": open(zip_path, "rb")
    }

    response = requests.post(
        url,
        headers=headers,
        data=data,
        files=files,
        timeout=120
    )

    if response.status_code not in (200, 201):
        raise RuntimeError(f"Payhip failed: {response.text}")

    print("✅ Payhip publish success")
    return {
        "platform": "payhip",
        "status": "success",
        "response": response.json()
    }
