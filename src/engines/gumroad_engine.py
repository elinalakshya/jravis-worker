# src/engines/gumroad_engine.py

import os
import requests
import time

GUMROAD_API_KEY = os.getenv("GUMROAD_API_KEY")
PRODUCT_ID = os.getenv("GUMROAD_PRODUCT_ID")

BASE_URL = "https://api.gumroad.com/v2"

HEADERS = {
    "Authorization": f"Bearer {GUMROAD_API_KEY}"
}

class GumroadError(Exception):
    pass


def upload_file_to_product(zip_path: str, title: str):
    if not PRODUCT_ID:
        raise GumroadError("GUMROAD_PRODUCT_ID is missing")

    print(f"📦 Updating Gumroad product → {PRODUCT_ID}")
    print(f"📤 Upload source = {zip_path}")

    # 1️⃣ Upload / replace file
    with open(zip_path, "rb") as f:
        files = {
            "file": f
        }

        data = {
            "product_id": PRODUCT_ID
        }

        r = requests.post(
            f"{BASE_URL}/products/{PRODUCT_ID}/files",
            headers=HEADERS,
            files=files,
            data=data,
            timeout=60
        )

    if r.status_code != 200:
        raise GumroadError(f"File upload failed: {r.text}")

    # 2️⃣ Update product name / description (optional but clean)
    payload = {
        "name": title,
        "description": f"Auto-updated content by JRAVIS\n\nLast update: {time.ctime()}"
    }

    r2 = requests.put(
        f"{BASE_URL}/products/{PRODUCT_ID}",
        headers=HEADERS,
        data=payload,
        timeout=30
    )

    if r2.status_code != 200:
        raise GumroadError(f"Product update failed: {r2.text}")

    print("✅ Gumroad product updated successfully")
    return {"gumroad": "success"}
