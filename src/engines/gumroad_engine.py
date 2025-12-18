import os
import requests

GUMROAD_API_KEY = os.getenv("GUMROAD_API_KEY")
GUMROAD_API_BASE = "https://api.gumroad.com/v2"

DEFAULT_PRICE = int(os.getenv("GUMROAD_PRICE", "9"))  # USD
DEFAULT_CURRENCY = os.getenv("GUMROAD_CURRENCY", "usd")


class GumroadError(Exception):
    pass


def create_gumroad_product(
    title: str,
    content_url: str,
    description: str = "",
    price: int = DEFAULT_PRICE,
    currency: str = DEFAULT_CURRENCY,
):
    """
    Creates a NEW Gumroad product with external content URL.
    This is the ONLY supported automation method by Gumroad.
    """

    if not GUMROAD_API_KEY:
        raise GumroadError("GUMROAD_API_KEY is missing")

    url = f"{GUMROAD_API_BASE}/products"

    payload = {
        "access_token": GUMROAD_API_KEY,
        "name": title,
        "price": price,
        "currency": currency,
        "description": description or f"Digital download: {title}",
        "content_url": content_url,
        "published": True,
    }

    response = requests.post(url, data=payload, timeout=30)

    if response.status_code != 200:
        raise GumroadError(
            f"Gumroad create failed [{response.status_code}]: {response.text}"
        )

    data = response.json()

    if not data.get("success"):
        raise GumroadError(f"Gumroad API error: {data}")

    product = data.get("product", {})
    product_id = product.get("id")
    short_url = product.get("short_url")

    return {
        "status": "success",
        "product_id": product_id,
        "url": short_url,
    }
