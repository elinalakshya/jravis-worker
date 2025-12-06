# -----------------------------------------------------------
# PAYHIP PUBLISHER — JRAVIS Phase-1 Template Marketplace
# -----------------------------------------------------------

import os
import requests

PAYHIP_API_KEY = os.getenv("PAYHIP_API_KEY", "")

def upload_to_payhip(zip_path: str, title: str):
    print(f"[PAYHIP] Uploading {title}...")

    if not PAYHIP_API_KEY:
        print("[PAYHIP] ❌ Missing API Key")
        return {"status": "error"}

    try:
        url = "https://payhip.com/api/v1/products/create"

        files = {"file": open(zip_path, "rb")}

        data = {
            "name": title,
            "price": "6.00",
            "description": "JRAVIS Automated Template"
        }

        headers = {"Authorization": PAYHIP_API_KEY}

        r = requests.post(url, data=data, files=files, headers=headers)
        print("[PAYHIP] Response:", r.text)

        return {"status": "ok", "response": r.text}

    except Exception as e:
        print("[PAYHIP] ERROR:", e)
        return {"status": "error", "reason": str(e)}
