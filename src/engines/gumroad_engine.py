import os
import requests

GUMROAD_API = "https://api.gumroad.com/v2/products"

def create_gumroad_product(title: str, content_url: str, price_usd: int = 9):
    api_key = os.environ["GUMROAD_API_KEY"]

    payload = {
        "access_token": api_key,
        "name": title,
        "price": price_usd * 100,   # cents
        "content_url": content_url,
        "published": True
    }

    print("🛒 Creating Gumroad product...")

    r = requests.post(GUMROAD_API, data=payload, timeout=30)

    if r.status_code != 200:
        raise Exception(f"Gumroad create failed [{r.status_code}]: {r.text}")

    product = r.json()["product"]

    print("🆔 Gumroad Product ID =", product["id"])
    print("🔗 Product URL =", product["short_url"])

    return product
