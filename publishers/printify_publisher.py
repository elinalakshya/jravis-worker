import os
import requests
import json

PRINTIFY_API_KEY = os.getenv("PRINTIFY_API_KEY")

# If you know your shop ID, set it here — otherwise JRAVIS will auto-fetch.
PRINTIFY_SHOP_ID = os.getenv("PRINTIFY_SHOP_ID")


def get_shop_id():
    """Fetch the user's Printify shop ID if not provided."""
    if PRINTIFY_SHOP_ID:
        return PRINTIFY_SHOP_ID

    try:
        res = requests.get(
            "https://api.printify.com/v1/shops.json",
            headers={"Authorization": f"Bearer {PRINTIFY_API_KEY}"}
        ).json()

        if isinstance(res, list) and len(res) > 0:
            return res[0]["id"]

    except Exception:
        return None

    return None


def create_printify_product(title, description, image_url):
    """
    Creates a new Printify product using a POD blank + artwork.
    NOTE: This creates an internal product (not published to Shopify yet).
    """

    shop_id = get_shop_id()
    if not shop_id:
        return {"status": "error", "message": "Unable to fetch Printify shop ID"}

    try:
        payload = {
            "title": title,
            "description": description,
            "print_provider_id": 1,  # Printify internal provider (default)
            "blueprint_id": 6,       # Example: Unisex T-Shirt
            "variants": [
                {
                    "id": 4012,  # default variant
                    "price": 1499,
                }
            ],
            "print_areas": [
                {
                    "variant_ids": [4012],
                    "placeholders": [
                        {"position": "front", "images": [image_url]}
                    ]
                }
            ]
        }

        res = requests.post(
            f"https://api.printify.com/v1/shops/{shop_id}/products.json",
            headers={
                "Authorization": f"Bearer {PRINTIFY_API_KEY}",
                "Content-Type": "application/json"
            },
            data=json.dumps(payload)
        ).json()

        if "id" not in res:
            return {"status": "error", "message": res}

        return {
            "status": "success",
            "product_id": res["id"],
            "title": title,
            "printify_url": f"https://printify.com/app/products/{res['id']}"
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
