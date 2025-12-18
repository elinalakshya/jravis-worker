# ==========================================
# JRAVIS UNIFIED ENGINE – CONTENT_URL MODE
# ==========================================

import os
import time

from engines.gumroad_engine import update_gumroad_content_url

# ------------------------------------------
# CONFIG (FROM ENV)
# ------------------------------------------
R2_PUBLIC_BASE_URL = os.getenv("R2_PUBLIC_BASE_URL")
GUMROAD_PRODUCT_ID = os.getenv("GUMROAD_PRODUCT_ID")

if not R2_PUBLIC_BASE_URL:
    raise RuntimeError("❌ R2_PUBLIC_BASE_URL not set")

if not GUMROAD_PRODUCT_ID:
    raise RuntimeError("❌ GUMROAD_PRODUCT_ID not set")

# ------------------------------------------
# MAIN ENGINE
# ------------------------------------------
def run_all_streams_micro_engine(zip_path: str, template_name: str, backend: str):
    """
    CONTENT_URL MODE:
    - ZIP already exists in R2
    - Gumroad product already exists
    - Only update content_url
    """

    print(f"🚀 unified_engine START for {template_name}")

    if not os.path.exists(zip_path):
        raise FileNotFoundError(f"❌ ZIP not found: {zip_path}")

    filename = os.path.basename(zip_path)
    content_url = f"{R2_PUBLIC_BASE_URL}/{filename}"

    print(f"☁️ Using R2 asset")
    print(f"🔗 CONTENT URL = {content_url}")
    print(f"🛒 Gumroad Product ID = {GUMROAD_PRODUCT_ID}")

    # --------------------------------------
    # UPDATE GUMROAD CONTENT URL
    # --------------------------------------
    result = update_gumroad_content_url(
        product_id=GUMROAD_PRODUCT_ID,
        content_url=content_url
    )

    print("📊 ENGINE COMPLETE:", result)

    return result
