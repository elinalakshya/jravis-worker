import os
from engines.gumroad_engine import update_gumroad_content_url

def run_all_streams_micro_engine(zip_path: str, template_name: str, backend_url: str = None):
    """
    backend_url is passed by worker.py — kept for compatibility
    """

    print(f"🚀 unified_engine START for {template_name}")

    PRODUCT_ID = os.getenv("GUMROAD_PRODUCT_ID")
    R2_PUBLIC_BASE_URL = os.getenv("R2_PUBLIC_BASE_URL")

    if not PRODUCT_ID:
        raise Exception("❌ GUMROAD_PRODUCT_ID missing")

    if not R2_PUBLIC_BASE_URL:
        raise Exception("❌ R2_PUBLIC_BASE_URL missing")

    filename = os.path.basename(zip_path)
    content_url = f"{R2_PUBLIC_BASE_URL}/{filename}"

    print("☁️ Using R2 asset")
    print(f"🔗 CONTENT URL = {content_url}")
    print(f"🛒 Gumroad Product ID = {PRODUCT_ID}")
    print("🛒 Updating Gumroad product content_url")

    result = update_gumroad_content_url(
        product_id=PRODUCT_ID,
        content_url=content_url
    )

    print("📊 ENGINE COMPLETE:", result)
    return {"gumroad": "success"}
