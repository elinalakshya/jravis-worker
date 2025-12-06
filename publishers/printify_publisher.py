# -----------------------------------------------------------
# PRINTIFY PUBLISHER — JRAVIS POD UPLOADER
# -----------------------------------------------------------

import os
import requests

PRINTIFY_API_KEY = os.getenv("PRINTIFY_API_KEY", "")
PRINTIFY_SHOP_ID = os.getenv("PRINTIFY_SHOP_ID", "")

def upload_to_printify(zip_path: str, title: str):
    print(f"[PRINTIFY] Uploading POD asset for {title}...")

    if not PRINTIFY_API_KEY:
        print("[PRINTIFY] ❌ Missing API Key")
        return {"status": "error"}

    try:
        headers = {
            "Authorization": f"Bearer {PRINTIFY_API_KEY}",
            "Content-Type": "application/json"
        }

        url = f"https://api.printify.com/v1/shops/{PRINTIFY_SHOP_ID}/products.json"

        payload = {
            "title": title,
            "description": "JRAVIS Automated POD Product",
            "blueprint_id": 6,
            "print_provider_id": 1,
            "variants": []
        }

        r = requests.post(url, json=payload, headers=headers)
        print("[PRINTIFY] Response:", r.text)

        return {"status": "ok", "response": r.text}

    except Exception as e:
        print("[PRINTIFY] ERROR:", e)
        return {"status": "error", "reason": str(e)}
