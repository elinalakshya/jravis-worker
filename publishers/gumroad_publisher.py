import os
import requests

GUMROAD_API_KEY = os.getenv("GUMROAD_API_KEY")

GUMROAD_CREATE_URL = "https://api.gumroad.com/v2/products"
GUMROAD_UPLOAD_URL = "https://api.gumroad.com/v2/products/{}/files"


def upload_to_gumroad(name, description, price, zip_path):
    """
    Uploads a template ZIP to Gumroad and publishes the product.
    """

    if not GUMROAD_API_KEY:
        return {"status": "error", "message": "Missing Gumroad API key"}

    try:
        # Step 1: Create product
        create_payload = {
            "access_token": GUMROAD_API_KEY,
            "name": name,
            "description": description,
            "price": int(price * 100),  # Gumroad expects cents
            "published": True
        }

        create_res = requests.post(GUMROAD_CREATE_URL, data=create_payload).json()

        if not create_res.get("success"):
            return {"status": "error", "message": create_res}

        product_id = create_res["product"]["id"]

        # Step 2: Upload ZIP file
        with open(zip_path, "rb") as f:
            files = {"file": (os.path.basename(zip_path), f, "application/zip")}
            upload_payload = {"access_token": GUMROAD_API_KEY}

            upload_res = requests.post(
                GUMROAD_UPLOAD_URL.format(product_id),
                data=upload_payload,
                files=files
            ).json()

        if not upload_res.get("success"):
            return {"status": "error", "message": upload_res}

        # Step 3: Return product URL
        product_url = create_res["product"]["short_url"]

        return {
            "status": "success",
            "product_id": product_id,
            "product_url": product_url
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
