# -----------------------------------------------------------
# JRAVIS — Gumroad Auto Publisher
# Mission 2040 — Template Marketplace (Phase 1)
# -----------------------------------------------------------

import os
import requests

GUMROAD_TOKEN = os.getenv("GUMROAD_API_KEY")
GUMROAD_PRICE = 1200  # $12 → Gumroad uses cents

BASE_URL = "https://api.gumroad.com/v2"


# -----------------------------------------------------------
# Create Product
# -----------------------------------------------------------
def create_gumroad_product(title, description):
    try:
        url = f"{BASE_URL}/products"
        payload = {
            "access_token": GUMROAD_TOKEN,
            "name": title,
            "description": description,
            "price": GUMROAD_PRICE,
            "custom_receipt": "Thanks for supporting JRAVIS Automation!",
            "published": True
        }

        resp = requests.post(url, data=payload, timeout=20)
        data = resp.json()

        if not data.get("success"):
            print("[Gumroad] ❌ Product creation failed:", data)
            return None

        return data["product"]["id"]

    except Exception as e:
        print("[Gumroad] ❌ Error creating product:", e)
        return None


# -----------------------------------------------------------
# Upload File (ZIP Template)
# -----------------------------------------------------------
def upload_file(product_id, file_path):
    try:
        url = f"{BASE_URL}/products/{product_id}"
        files = {
            "content": (os.path.basename(file_path), open(file_path, "rb"))
        }

        payload = {
            "access_token": GUMROAD_TOKEN
        }

        resp = requests.put(url, data=payload, files=files, timeout=30)
        return resp.json()

    except Exception as e:
        print("[Gumroad] ❌ Upload failed:", e)
        return None


# -----------------------------------------------------------
# Add Cover Image
# -----------------------------------------------------------
def add_cover_image(product_id, image_path):
    try:
        url = f"{BASE_URL}/products/{product_id}"
        files = {
            "preview_file": (os.path.basename(image_path), open(image_path, "rb"))
        }

        payload = {
            "access_token": GUMROAD_TOKEN
        }

        resp = requests.put(url, data=payload, files=files, timeout=30)
        return resp.json()

    except Exception as e:
        print("[Gumroad] ❌ Cover image upload failed:", e)
        return None


# -----------------------------------------------------------
# MAIN ENTRY — Called by Unified Engine
# -----------------------------------------------------------
def publish_to_gumroad(template_name, zip_path, cover_image):
    print(f"[Gumroad] 🚀 Publishing {template_name} to Gumroad...")

    if not GUMROAD_TOKEN:
        return {"status": "error", "message": "Missing GUMROAD_API_KEY"}

    # Step 1: Create Product
    product_id = create_gumroad_product(
        title=f"{template_name} — JRAVIS Auto Template",
        description="Premium automated design template by JRAVIS. Instant download & commercial use."
    )

    if not product_id:
        return {"status": "error", "message": "Product creation failed"}

    # Step 2: Upload ZIP File
    upload_file(product_id, zip_path)

    # Step 3: Upload Cover Image
    add_cover_image(product_id, cover_image)

    product_url = f"https://gumroad.com/l/{product_id}"

    print(f"[Gumroad] ✅ Uploaded Successfully → {product_url}")

    return {
        "status": "success",
        "url": product_url,
        "product_id": product_id
    }
