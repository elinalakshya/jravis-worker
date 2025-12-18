import os
import requests

GUMROAD_API_KEY = os.getenv("GUMROAD_API_KEY")
GUMROAD_PRODUCT_ID = os.getenv("GUMROAD_PRODUCT_ID")

GUMROAD_BASE = "https://api.gumroad.com/v2"


def update_gumroad_product(zip_path: str, title: str, description: str):
    if not GUMROAD_API_KEY or not GUMROAD_PRODUCT_ID:
        raise Exception("Missing Gumroad API key or Product ID")

    # 1️⃣ Update product metadata
    meta_resp = requests.put(
        f"{GUMROAD_BASE}/products/{GUMROAD_PRODUCT_ID}",
        data={
            "access_token": GUMROAD_API_KEY,
            "name": title,
            "description": description,
        },
        timeout=60,
    )

    if not meta_resp.ok:
        raise Exception(f"Metadata update failed: {meta_resp.text}")

    # 2️⃣ Upload new file (this REPLACES existing file)
    with open(zip_path, "rb") as f:
        file_resp = requests.post(
            f"{GUMROAD_BASE}/products/{GUMROAD_PRODUCT_ID}/files",
            data={"access_token": GUMROAD_API_KEY},
            files={"file": f},
            timeout=300,
        )

    if not file_resp.ok:
        raise Exception(f"File upload failed: {file_resp.text}")

    return {
        "status": "success",
        "product_id": GUMROAD_PRODUCT_ID,
    }
