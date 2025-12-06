# -----------------------------------------------------------
# JRAVIS — Printify Auto Publisher (T-Shirt Mode)
# Mission 2040 Phase-1 Monetization Engine
# -----------------------------------------------------------

import requests
import os
import base64

PRINTIFY_API_KEY = os.getenv("PRINTIFY_API_KEY")
PRINTIFY_SHOP_ID = os.getenv("PRINTIFY_SHOP_ID")

HEADERS = {
    "Authorization": f"Bearer {PRINTIFY_API_KEY}",
    "Content-Type": "application/json"
}

BASE_URL = "https://api.printify.com/v1"


# -----------------------------------------------------------
# Fetch T-Shirt Blueprint
# -----------------------------------------------------------
def fetch_tshirt_blueprint():
    try:
        url = f"{BASE_URL}/catalog/blueprints.json"
        resp = requests.get(url, headers=HEADERS, timeout=20)

        for item in resp.json():
            if "t-shirt" in item["title"].lower():
                return item["id"]

        return None
    except Exception as e:
        print("[Printify] ❌ Error fetching blueprints:", e)
        return None


# -----------------------------------------------------------
# Fetch Print Provider for Blueprint
# -----------------------------------------------------------
def get_provider_for_blueprint(blueprint_id):
    try:
        url = f"{BASE_URL}/catalog/blueprints/{blueprint_id}/print_providers.json"
        resp = requests.get(url, headers=HEADERS, timeout=20)
        providers = resp.json()

        if providers:
            return providers[0]["id"]  # pick first provider
        return None
    except Exception as e:
        print("[Printify] ❌ Error fetching provider:", e)
        return None


# -----------------------------------------------------------
# Fetch Variant (Size/Color)
# -----------------------------------------------------------
def get_variant(blueprint_id, provider_id):
    try:
        url = f"{BASE_URL}/catalog/blueprints/{blueprint_id}/print_providers/{provider_id}.json"
        resp = requests.get(url, headers=HEADERS, timeout=20)

        variants = resp.json().get("variants", [])
        if variants:
            return variants[0]["id"]  # pick first variant
        return None
    except Exception as e:
        print("[Printify] ❌ Error fetching variants:", e)
        return None


# -----------------------------------------------------------
# Upload Artwork
# -----------------------------------------------------------
def upload_artwork(image_path):
    try:
        with open(image_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()

        payload = {
            "file_name": os.path.basename(image_path),
            "contents": encoded
        }

        url = f"{BASE_URL}/uploads/images.json"
        resp = requests.post(url, json=payload, headers=HEADERS, timeout=20)

        return resp.json().get("id")
    except Exception as e:
        print("[Printify] ❌ Artwork upload failed:", e)
        return None


# -----------------------------------------------------------
# Create Product
# -----------------------------------------------------------
def create_printify_product(blueprint_id, provider_id, variant_id, artwork_id, title):
    try:
        payload = {
            "title": title,
            "description": "Automated JRAVIS T-Shirt — Mission 2040",
            "blueprint_id": blueprint_id,
            "print_provider_id": provider_id,
            "variants": [
                {"id": variant_id, "price": 1500, "is_enabled": True}
            ],
            "print_areas": [
                {
                    "variant_ids": [variant_id],
                    "placeholders": [
                        {"position": "front", "images": [{"id": artwork_id, "x": 0.5, "y": 0.5, "scale": 1}]}
                    ]
                }
            ]
        }

        url = f"{BASE_URL}/shops/{PRINTIFY_SHOP_ID}/products.json"
        resp = requests.post(url, json=payload, headers=HEADERS, timeout=20)
        return resp.json()
    except Exception as e:
        print("[Printify] ❌ Product creation failed:", e)
        return None


# -----------------------------------------------------------
# Publish Product to Store
# -----------------------------------------------------------
def publish_product(product_id):
    try:
        url = f"{BASE_URL}/shops/{PRINTIFY_SHOP_ID}/products/{product_id}/publish.json"
        payload = {
            "title": True,
            "description": True,
            "images": True,
            "variants": True
        }
        resp = requests.post(url, json=payload, headers=HEADERS, timeout=20)
        return resp.json()
    except Exception as e:
        print("[Printify] ❌ Publishing failed:", e)
        return None


# -----------------------------------------------------------
# MAIN ENTRY — Called by Unified Engine
# -----------------------------------------------------------
def publish_to_printify(template_name, image_path):
    print(f"[Printify] 👕 Publishing T-Shirt for {template_name}...")

    if not PRINTIFY_API_KEY:
        return {"status": "error", "message": "Missing PRINTIFY_API_KEY"}

    blueprint = fetch_tshirt_blueprint()
    if not blueprint:
        return {"status": "error", "message": "No blueprint found"}

    provider = get_provider_for_blueprint(blueprint)
    if not provider:
        return {"status": "error", "message": "No provider found"}

    variant = get_variant(blueprint, provider)
    if not variant:
        return {"status": "error", "message": "No variant found"}

    artwork = upload_artwork(image_path)
    if not artwork:
        return {"status": "error", "message": "Artwork upload failed"}

    product = create_printify_product(
        blueprint, provider, variant, artwork, f"JRAVIS — {template_name}"
    )

    if not product or "id" not in product:
        return {"status": "error", "message": "Product creation failed"}

    publish = publish_product(product["id"])

    print("[Printify] ✅ Published successfully!")
    return {
        "status": "success",
        "product_id": product["id"],
        "publish_result": publish
    }
