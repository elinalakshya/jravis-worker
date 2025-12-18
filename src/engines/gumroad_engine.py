import os
import requests

GUMROAD_API_KEY = os.getenv("GUMROAD_API_KEY")

def upload_file_to_product(product_id: str, zip_path: str):
    """
    Uploads ZIP file to an EXISTING Gumroad product
    """

    if not os.path.exists(zip_path):
        raise FileNotFoundError(f"ZIP path does not exist: {zip_path}")

    url = f"https://api.gumroad.com/v2/products/{product_id}"

    headers = {
        "Authorization": f"Bearer {GUMROAD_API_KEY}"
    }

    files = {
        "file": open(zip_path, "rb")
    }

    data = {
        "published": "true"
    }

    response = requests.put(url, headers=headers, files=files, data=data)

    if response.status_code not in (200, 201):
        raise RuntimeError(f"Gumroad upload failed: {response.text}")

    return "success"
