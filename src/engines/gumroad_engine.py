import os
import requests

GUMROAD_API_KEY = os.getenv("GUMROAD_API_KEY")


def upload_file_to_product(product_id: str, zip_path: str):
    """
    Correct Gumroad API:
    POST /products/{product_id}/files
    """

    if not os.path.exists(zip_path):
        raise FileNotFoundError(f"ZIP not found: {zip_path}")

    url = f"https://api.gumroad.com/v2/products/{product_id}/files"

    headers = {
        "Authorization": f"Bearer {GUMROAD_API_KEY}"
    }

    files = {
        "file": open(zip_path, "rb")
    }

    response = requests.post(
        url,
        headers=headers,
        files=files,
        timeout=60
    )

    if response.status_code not in (200, 201):
        raise RuntimeError(
            f"Gumroad upload failed [{response.status_code}]: {response.text}"
        )

    print("✅ Gumroad file uploaded successfully")
    return "success"
