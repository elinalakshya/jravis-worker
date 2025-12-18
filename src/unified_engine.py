import os
from engines.gumroad_engine import update_gumroad_content_url
from engines.r2_engine import upload_file_to_r2


PRODUCT_ID = os.getenv("GUMROAD_PRODUCT_ID")
R2_PUBLIC_BASE_URL = os.getenv("R2_PUBLIC_BASE_URL")

if not PRODUCT_ID:
    raise RuntimeError("❌ GUMROAD_PRODUCT_ID not set")

if not R2_PUBLIC_BASE_URL:
    raise RuntimeError("❌ R2_PUBLIC_BASE_URL not set")


def run_all_streams_micro_engine(zip_path: str, template_name: str):
    print(f"🚀 unified_engine START for {template_name}")
    print("☁️ Using R2 asset")

    # -----------------------------
    # Upload to R2
    # -----------------------------
    object_key = os.path.basename(zip_path)

    upload_file_to_r2(
        local_path=zip_path,
        object_key=object_key
    )

    content_url = f"{R2_PUBLIC_BASE_URL}/{object_key}"

    print("🔗 CONTENT URL =", content_url)
    print("🛒 Gumroad Product ID =", PRODUCT_ID)

    # -----------------------------
    # Update Gumroad product
    # -----------------------------
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
