# -----------------------------------------------------------
# JRAVIS Unified Monetization Engine (FINAL)
# Handles: ZIP Download → Gumroad → Payhip → Printify → Newsletter → Funnel → Marketplaces
# -----------------------------------------------------------

import os
import requests

from publishers.gumroad_publisher import publish_to_gumroad
from publishers.payhip_publisher import publish_to_payhip
from publishers.printify_publisher import publish_to_printify
from publishers.newsletter_publisher import send_newsletter
from publishers.affiliate_funnel_publisher import create_affiliate_funnel
from publishers.multi_marketplace_publisher import publish_to_marketplaces


# -----------------------------------------------------------
# Extract human title from template ZIP
# -----------------------------------------------------------
def extract_title(zip_path: str) -> str:
    base = os.path.basename(zip_path)
    name = base.replace(".zip", "").replace("_", " ").title()
    return name


# -----------------------------------------------------------
# MAIN ENGINE — accepts 3 arguments
# -----------------------------------------------------------
def run_all_streams_micro_engine(zip_path: str, template_name: str, backend_url: str):
    print("\n⚙️ JRAVIS UNIFIED ENGINE STARTED")
    print(f"📦 Input ZIP → {zip_path}")

    # Convert ZIP filename → polished title
    title = extract_title(zip_path)
    print(f"📝 Title → {title}")

    # -----------------------------------------------------------
    # 1) Download ZIP from Backend
    # -----------------------------------------------------------
    download_url = f"{backend_url}/{zip_path}"
    print(f"[DOWNLOAD] Fetching ZIP from {download_url}")

    try:
        response = requests.get(download_url)
        if response.status_code != 200:
            print("[DOWNLOAD ERROR]", response.text)
            return {"status": "failed", "reason": "zip_download_failed"}
    except Exception as e:
        print("[DOWNLOAD EXCEPTION]", e)
        return {"status": "failed", "reason": "zip_exception"}

    # Save ZIP locally
    local_zip_path = f"/tmp/{os.path.basename(zip_path)}"
    with open(local_zip_path, "wb") as f:
        f.write(response.content)

    print(f"[DOWNLOAD] Saved ZIP to {local_zip_path}")

    # -----------------------------------------------------------
    # 2) Gumroad Upload
    # -----------------------------------------------------------
    print("\n🚀 Uploading to Gumroad...")
    gumroad_res = publish_to_gumroad(local_zip_path, title)

    try:
        gumroad_link = gumroad_res.get("url", "https://gumroad.com")
    except:
        gumroad_link = "https://gumroad.com"

    # -----------------------------------------------------------
    # 3) Payhip Upload
    # -----------------------------------------------------------
    print("\n🚀 Uploading to Payhip...")
    payhip_res = publish_to_payhip(local_zip_path, title)

    # -----------------------------------------------------------
    # 4) Printify POD Upload
    # -----------------------------------------------------------
    print("\n👕 Sending artwork to Printify...")
    printify_res = publish_to_printify(local_zip_path, title)

    # -----------------------------------------------------------
    # 5) Newsletter Promotion
    # -----------------------------------------------------------
    print("\n📧 Sending Newsletter Blast...")
    newsletter_res = send_newsletter(title, gumroad_link)

    # -----------------------------------------------------------
    # 6) Affiliate Funnel Creation
    # -----------------------------------------------------------
    print("\n🌀 Creating Affiliate Funnel Page...")
    funnel_res = create_affiliate_funnel(title, gumroad_link)

    # -----------------------------------------------------------
    # 7) Marketplace Distribution
    # -----------------------------------------------------------
    print("\n🌍 Publishing to Multi-Marketplaces...")
    marketplace_res = publish_to_marketplaces(local_zip_path, title)

    # -----------------------------------------------------------
    # SUMMARY
    # -----------------------------------------------------------
    print("\n🎉 MONETIZATION COMPLETE")
    print("--------------------------------")
    print("Gumroad →", gumroad_res.get("status"))
    print("Payhip →", payhip_res.get("status"))
    print("Printify →", printify_res.get("status"))
    print("Newsletter →", newsletter_res.get("status"))
    print("Funnel →", funnel_res.get("status"))
    print("Marketplaces →", marketplace_res.get("status"))
    print("--------------------------------\n")

    return {
        "gumroad": gumroad_res,
        "payhip": payhip_res,
        "printify": printify_res,
        "newsletter": newsletter_res,
        "funnel": funnel_res,
        "marketplaces": marketplace_res
    }
