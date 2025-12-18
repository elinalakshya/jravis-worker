import os
from engines.gumroad_engine import create_gumroad_product

R2_PUBLIC_BASE_URL = os.getenv("R2_PUBLIC_BASE_URL")


def run_all_streams_micro_engine(template_name: str, zip_path: str):
    """
    Unified publishing engine
    """

    print(f"🚀 unified_engine START for {template_name}")

    if not R2_PUBLIC_BASE_URL:
        raise RuntimeError("R2_PUBLIC_BASE_URL not set")

    # Build public asset URL
    content_url = f"{R2_PUBLIC_BASE_URL}/{template_name}.zip"

    print("☁️ Using R2 asset")
    print(f"🔗 CONTENT URL = {content_url}")

    # Create Gumroad product
    print("🛒 Creating Gumroad product...")
    result = create_gumroad_product(
        title=template_name,
        content_url=content_url,
        description=f"Auto-generated digital product: {template_name}"
    )

    print("✅ Gumroad product created")
    print(f"🆔 Product ID: {result['product_id']}")
    print(f"🔗 Product URL: {result['url']}")

    return {
        "status": "published",
        "platform": "gumroad",
        "product_id": result["product_id"],
        "url": result["url"]
    }
