import os
import requests

PAYHIP_API_KEY = os.getenv("PAYHIP_API_KEY")

PAYHIP_PRODUCT_URL = "https://payhip.com/api/products"


def upload_to_payhip(name, description, price, zip_path):
    """
    Uploads a digital product (ZIP) to Payhip using their API.
    """

    if not PAYHIP_API_KEY:
        return {"status": "error", "message": "Missing Payhip API key"}

    try:
        # Prepare payload
        payload = {
            "api_key": PAYHIP_API_KEY,
            "title": name,
            "description": description,
            "price": float(price),
            "published": "true"
        }

        # Attach file
        with open(zip_path, "rb") as file:
            files = {
                "file": (os.path.basename(zip_path), file, "application/zip")
            }

            response = requests.post(PAYHIP_PRODUCT_URL, data=payload, files=files)

        try:
            res = response.json()
        except:
            return {"status": "error", "message": "Invalid JSON response from Payhip"}

        if "error" in res:
            return {"status": "error", "message": res["error"]}

        # Product created
        product_url = f"https://payhip.com/b/{res.get('product_id')}"

        return {
            "status": "success",
            "product_id": res.get("product_id"),
            "product_url": product_url
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
