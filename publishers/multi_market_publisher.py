# -----------------------------------------------------------
# JRAVIS — Multi Marketplace Uploader (Etsy, CM, DB, CF)
# Mission 2040 — Global Passive Income Engine
# -----------------------------------------------------------

import os
import json
import requests
import shutil

OUTPUT_DIR = "marketplace_packages"
os.makedirs(OUTPUT_DIR, exist_ok=True)

ETSY_API_KEY = os.getenv("ETSY_API_KEY")
ETSY_SHOP_ID = os.getenv("ETSY_SHOP_ID")

CF_API_KEY = os.getenv("CREATIVE_FABRICA_KEY")
CM_EMAIL = os.getenv("CM_EMAIL")
CM_PASSWORD = os.getenv("CM_PASSWORD")

# -----------------------------------------------------------
# Marketplace Metadata Generator
# -----------------------------------------------------------
def generate_metadata(template_name):
    title = f"{template_name} — Premium Business Template"
    description = (
        f"{template_name} is a professionally generated design template by JRAVIS Automation.\n"
        "Perfect for digital creators, small businesses, and online sellers.\n"
        "Includes commercial rights."
    )
    tags = [
        "template", "business", "digital download", "branding",
        "jrvis", "automation", "design", "creative"
    ]

    return {
        "title": title,
        "description": description,
        "tags": tags
    }


# -----------------------------------------------------------
# Package ZIP for Marketplaces
# -----------------------------------------------------------
def prepare_marketplace_zip(template_name, zip_path):
    out_path = os.path.join(OUTPUT_DIR, f"{template_name}-market.zip")
    shutil.copy(zip_path, out_path)
    return out_path


# -----------------------------------------------------------
# Etsy Upload (Requires Keys)
# -----------------------------------------------------------
def upload_to_etsy(metadata, marketplace_zip):
    if not ETSY_API_KEY or not ETSY_SHOP_ID:
        return {"status": "skipped", "reason": "Missing Etsy API Key"}

    try:
        url = f"https://openapi.etsy.com/v3/application/shops/{ETSY_SHOP_ID}/listings"

        payload = {
            "title": metadata["title"],
            "description": metadata["description"],
            "price": 12.0,
            "quantity": 999,
            "who_made": "i_did",
            "is_supply": False,
            "when_made": "made_to_order"
        }

        headers = {
            "x-api-key": ETSY_API_KEY,
            "Content-Type": "application/json"
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=20)

        return resp.json()

    except Exception as e:
        return {"status": "error", "reason": str(e)}


# -----------------------------------------------------------
# Creative Fabrica Upload
# -----------------------------------------------------------
def upload_to_creative_fabrica(metadata, marketplace_zip):
    if not CF_API_KEY:
        return {"status": "skipped", "reason": "Missing Creative Fabrica API Key"}

    try:
        url = "https://api.creativefabrica.com/v1/upload"

        files = {
            "file": (os.path.basename(marketplace_zip), open(marketplace_zip, "rb"))
        }

        payload = {
            "api_key": CF_API_KEY,
            "title": metadata["title"],
            "description": metadata["description"]
        }

        resp = requests.post(url, data=payload, files=files, timeout=20)
        return resp.json()

    except Exception as e:
        return {"status": "error", "reason": str(e)}


# -----------------------------------------------------------
# Placeholder for CreativeMarket (manual upload automation)
# -----------------------------------------------------------
def upload_to_creativemarket(metadata, marketplace_zip):
    if not CM_EMAIL or not CM_PASSWORD:
        return {"status": "skipped", "reason": "Missing CreativeMarket Credentials"}

    # NOTE: Official API does not exist.
    # JRAVIS prepares the file; actual upload can be semi-automated via Selenium later.

    return {"status": "ready", "file": marketplace_zip}


# -----------------------------------------------------------
# MAIN ENTRY — Called by JRAVIS Unified Engine
# -----------------------------------------------------------
def publish_to_marketplaces(template_name, zip_path):
    print(f"[Marketplaces] 🌍 Publishing {template_name} to global stores...")

    metadata = generate_metadata(template_name)
    marketplace_zip = prepare_marketplace_zip(template_name, zip_path)

    result = {
        "etsy": upload_to_etsy(metadata, marketplace_zip),
        "creative_fabrica": upload_to_creative_fabrica(metadata, marketplace_zip),
        "creative_market": upload_to_creativemarket(metadata, marketplace_zip)
    }

    print("[Marketplaces] ✅ Completed marketplace processing")
    return result
