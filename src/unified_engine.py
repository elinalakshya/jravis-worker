# ===============================
# JRAVIS UNIFIED ENGINE (FINAL)
# UPDATE-ONLY GUMROAD MODE
# ===============================

import os
import traceback

from engines.gumroad_engine import upload_file_to_product


def run_all_streams_micro_engine(zip_path: str, template_name: str, backend_url: str):
    """
    JRAVIS execution core
    - Uses EXISTING Gumroad product
    - Uploads new ZIP to same product
    - Fully automated
    """

    print(f"🚀 unified_engine START for {template_name}")

    # ---- BASIC VALIDATION ----
    if not os.path.exists(zip_path):
        raise FileNotFoundError(f"ZIP not found: {zip_path}")

    product_id = os.getenv("GUMROAD_PRODUCT_ID")
    if not product_id:
        raise RuntimeError("❌ GUMROAD_PRODUCT_ID not set in environment")

    results = {}

    # ===============================
    # GUMROAD UPDATE (NO CREATE)
    # ===============================
    try:
        print(f"📦 Updating Gumroad product → {product_id}")
        print(f"📤 Upload source = {zip_path}")

        # ✅ POSITIONAL CALL (CRITICAL FIX)
        result = upload_file_to_product(
            product_id,
            zip_path
        )

        results["gumroad"] = result
        print("✅ Gumroad product updated successfully")

    except Exception as e:
        print("❌ Gumroad update failed")
        traceback.print_exc()
        raise RuntimeError(f"gumroad failed: {e}")

    print(f"📊 ENGINE COMPLETE: {results}")
    return results
