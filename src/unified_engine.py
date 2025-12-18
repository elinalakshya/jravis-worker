import os
import uuid

from engines.gumroad_engine import update_gumroad_content_url
from engines.r2_engine import upload_file_to_r2


# REQUIRED ENV VARS
PRODUCT_ID = os.getenv("GUMROAD_PRODUCT_ID")
R2_PUBLIC_BASE_URL = os.getenv("R2_PUBLIC_BASE_URL")

if not PRODUCT_ID:
    raise RuntimeError("❌ GUMROAD_PRODUCT_ID not set")

if not R2_PUBLIC_BASE_URL:
    raise RuntimeError("❌ R2_PUBLIC_BASE_URL not set")


def run_all_streams_micro_engine(zip_path: str, template_name: str):
    """
    FINAL FLOW:
    1. Upload ZIP to R2
    2. Generate public content_url
    3. Update Gumroad product content_url
    """

    print(f"🚀 unified_engine START for {template_name}")
    print("☁️ Using R2 asset")

    # -------------------------------------------------
    # STEP 1 — Upload ZIP to R2
    # -------------------------------------------------
    object_key = os.path.basename(zip_path)

    upload_file_to_r2(
        local_path=zip_path,
        object_key=object_key
    )

    content_url = f"{R2_PUBLIC_BASE_URL}/{object_key}"

    print("🔗 CONTENT URL =", content_url)
    print("🛒 Gumroad Product ID =", PRODUCT_ID)

    # -------------------------------------------------
    # STEP 2 — Update Gumroad product
    # -------------------------------------------------
    print("🛒 Updating Gumroad product content_url")

    update_gumroad_content_url(
        PRODUCT_ID,
        content_url
    )

    print("✅ Gumroad product updated successfully")

    return {
        "status": "success",
        "product_id": PRODUCT_ID,
        "content_url": content_url
    }
