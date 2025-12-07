import os
import requests

PRINTIFY_API = os.getenv("PRINTIFY_API_KEY", "")
PRINTIFY_SHOP_ID = os.getenv("PRINTIFY_SHOP_ID", "")

def upload_to_printify(zip_path, title):
    if not PRINTIFY_API or not PRINTIFY_SHOP_ID:
        return {"status": "error", "msg": "Missing Printify credentials"}

    url = f"https://api.printify.com/v1/shops/{PRINTIFY_SHOP_ID}/products.json"

    headers = {"Authorization": f"Bearer {PRINTIFY_API}"}

    payload = {
        "title": title,
        "description": f"{title} by JRAVIS Auto POD System",
        "print_areas": [],
        "variants": [],
    }

    try:
        r = requests.post(url, json=payload, headers=headers)
        return {"status": "success", "response": r.json()}
    except Exception as e:
        return {"status": "error", "msg": str(e)}
