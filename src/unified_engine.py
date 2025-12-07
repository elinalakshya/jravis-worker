# -----------------------------------------------------------
# JRAVIS Unified Monetization Engine — Phase-1
# Auto Upload → POD → Newsletter → Funnel → Marketplace
# -----------------------------------------------------------

import os
import traceback

# -----------------------------------
# IMPORT ALL PUBLISHERS SAFELY
# -----------------------------------

def safe_import(module_name, function_name):
    """Import a function and return dummy function if missing."""
    try:
        module = __import__(module_name, fromlist=[function_name])
        return getattr(module, function_name)
    except Exception as e:
        print(f"⚠️ WARNING: Failed to import {module_name}.{function_name}: {e}")

        def dummy(*args, **kwargs):
            return {"status": "failed", "error": f"{module_name} missing"}
        return dummy


upload_to_gumroad = safe_import("publishers.gumroad_publisher", "upload_to_gumroad")
upload_to_payhip = safe_import("publishers.payhip_publisher", "upload_to_payhip")
upload_to_printify = safe_import("publishers.printify_publisher", "upload_to_printify")
send_newsletter = safe_import("publishers.newsletter_content_publisher", "send_newsletter")
create_affiliate_funnel = safe_import("publishers.affiliate_funnel_publisher", "create_affiliate_funnel")
publish_to_marketplaces = safe_import("publishers.multi_marketplace_publisher", "publish_to_marketplaces")


# -----------------------------------------------------------
# Extract Product Title
# -----------------------------------------------------------
def extract_title(zip_path: str) -> str:
    base = os.path.basename(zip_path)
    title = base.replace(".zip", "").replace("_", " ").title()
    return title


# -----------------------------------------------------------
# MASTER ENGINE
# -----------------------------------------------------------
def run_all_streams_micro_engine(zip_path: str, template_code: str):
    print("\n========================================")
    print("⚙️  JRAVIS UNIFIED MONETIZATION ENGINE STARTED")
    print("========================================")
    print(f"📦 Template ZIP: {zip_path}")
    print(f"🧩 Template Code: {template_code}")

    title = extract_title(zip_path)
    print(f"📝 Product Title: {title}")

    results = {}

    # -----------------------------------------------------------
    # 1️⃣ Upload to Gumroad
    # -----------------------------------------------------------
    print("\n🚀 Uploading to Gumroad…")
    try:
        gumroad_res = upload_to_gumroad(zip_path, title)
    except Exception:
        gumroad_res = {"status": "failed", "error": traceback.format_exc()}
    results["gumroad"] = gumroad_res

    # Extract product link if available
    try:
        gumroad_link = gumroad_res["response"]["product"]["short_url"]
    except:
        gumroad_link = "https://gumroad.com"

    # -----------------------------------------------------------
    # 2️⃣ Upload to Payhip
    # -----------------------------------------------------------
    print("\n🚀 Uploading to Payhip…")
    try:
        payhip_res = upload_to_payhip(zip_path, title)
    except Exception:
        payhip_res = {"status": "failed", "error": traceback.format_exc()}
    results["payhip"] = payhip_res

    # -----------------------------------------------------------
    # 3️⃣ Send to Printify POD
    # -----------------------------------------------------------
    print("\n👕 Creating Printify POD product…")
    try:
        printify_res = upload_to_printify(zip_path, title)
    except Exception:
        printify_res = {"status": "failed", "error": traceback.format_exc()}
    results["printify"] = printify_res

    # -----------------------------------------------------------
    # 4️⃣ Newsletter Promotion
    # -----------------------------------------------------------
    print("\n📧 Sending Newsletter Blast…")
    try:
        newsletter_res = send_newsletter(title, gumroad_link)
    except Exception:
        newsletter_res = {"status": "failed", "error": traceback.format_exc()}
    results["newsletter"] = newsletter_res

    # -----------------------------------------------------------
    # 5️⃣ Affiliate Funnel (HTML Page)
    # -----------------------------------------------------------
    print("\n🌀 Creating Affiliate Funnel…")
    try:
        funnel_res = create_affiliate_funnel(title, gumroad_link)
    except Exception:
        funnel_res = {"status": "failed", "error": traceback.format_exc()}
    results["funnel"] = funnel_res

    # -----------------------------------------------------------
    # 6️⃣ Multi-Marketplace Distribution
    # -----------------------------------------------------------
    print("\n🌍 Publishing to Multi-Marketplaces…")
    try:
        marketplace_res = publish_to_marketplaces(zip_path, title)
    except Exception:
        marketplace_res = {"status": "failed", "error": traceback.format_exc()}
    results["marketplaces"] = marketplace_res

    # -----------------------------------------------------------
    # COMPLETED
    # -----------------------------------------------------------
    print("\n========================================")
    print("🎉 JRAVIS PHASE-1 MONETIZATION COMPLETED")
    print("========================================")
    for key, res in results.items():
        print(f"{key.upper():<15} → {res.get('status', 'unknown')}")

    print("========================================\n")

    return results
