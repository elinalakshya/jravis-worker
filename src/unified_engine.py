# ===============================
# JRAVIS UNIFIED ENGINE (PROD)
# UPDATE-ONLY GUMROAD MODE
# ===============================

import os
import traceback

from engines.gumroad_engine import upload_file_to_product


def run_all_streams_micro_engine(zip_path: str, template_name: str, backend_url: str):
    """
    Central execution engine.
    - NEVER creates Gumroad products
    - ONLY updates existing product using PRODUCT_ID
    """

    print(f"🚀 unified_engine START for {template_name}")

    # ---- VALIDATION ----
    if not os.path.exists(zip_path):
        raise FileNotFoundError(f"ZIP not found: {zip_path}")

    product_id = os.getenv("GUMROAD_PRODUCT_ID")
    if not product_id:
        raise RuntimeError("GUMROAD_PRODUCT_ID not set in environment")

    results = {}

    # ===============================
    # GUMROAD UPDATE ENGINE (LIVE)
    # ===============================
    try:
        print(f"📦 Updating Gumroad product → {product_id}")
        print(f"📤 Upload source = {zip_path}")

        result = upload_file_to_product(
            product_id=product_id,
            zip_path=zip_path,
            title=template_name
        )

        results["gumroad"] = result
        print("✅ Gumroad product updated successfully")

    except Exception as e:
        print("❌ Gumroad update failed")
        traceback.print_exc()
        raise RuntimeError(f"gumroad failed: {e}")

    # ===============================
    # FINAL STATUS
    # ===============================
    print(f"📊 ENGINE COMPLETE: {results}")
    return results
