# -----------------------------------------------------------
# JRAVIS Unified Monetization Engine
# Phase-1 Auto Upload → Promotion → Funnel Generation
# -----------------------------------------------------------

import os
from publishers.gumroad_publisher import upload_to_gumroad
from publishers.payhip_publisher import upload_to_payhip
from publishers.printify_publisher import upload_to_printify
from publishers.newsletter_content_publisher import send_newsletter
from publishers.affiliate_funnel_publisher import create_affiliate_funnel
from publishers.multi_marketplace_publisher import publish_to_marketplaces


# -----------------------------------------------------------
# Helper — Extract product title from ZIP
# -----------------------------------------------------------
def extract_title(zip_path: str) -> str:
    base = os.path.basename(zip_path)
    name = base.replace(".zip", "").replace("_", " ").title()
    return name


# -----------------------------------------------------------
# Master Engine — Runs ALL monetization streams
# -----------------------------------------------------------
def run_all_streams_micro_engine(zip_path: str, template_code: str):
    print("\n⚙️  ENGINE STARTED — JRAVIS Unified Monetization System")
    print(f"📦 ZIP: {zip_path}")
    
    title = extract_title(zip_path)

    print(f"📝 Using Title: {title}")

    # -----------------------------------------------------------
    # 1) Gumroad Upload
    # -----------------------------------------------------------
    print("\n🚀 Uploading to Gumroad...")
    gumroad_res = upload_to_gumroad(zip_path, title)

    gumroad_link = None
    try:
        gumroad_link = gumroad_res["response"]["product"]["short_url"]
    except:
        gumroad_link = "https://gumroad.com"

    # -----------------------------------------------------------
    # 2) Payhip Upload
    # -----------------------------------------------------------
    print("\n🚀 Uploading to Payhip...")
    payhip_res = upload_to_payhip(zip_path, title)

    # -----------------------------------------------------------
    # 3) Printify POD Product
    # -----------------------------------------------------------
    print("\n👕 Sending artwork to Printify...")
    printify_res = upload_to_printify(zip_path, title)

    # -----------------------------------------------------------
    # 4) Newsletter Promotion
    # -----------------------------------------------------------
    print("\n📧 Sending Newsletter Blast...")
    newsletter_res = send_newsletter(title, gumroad_link)

    # -----------------------------------------------------------
    # 5) Affiliate Funnel (HTML File)
    # -----------------------------------------------------------
    print("\n🌀 Creating Affiliate Funnel Page...")
    funnel_res = create_affiliate_funnel(title, gumroad_link)

    # -----------------------------------------------------------
    # 6) Multi-Marketplace Distribution (placeholder)
    # -----------------------------------------------------------
    print("\n🌍 Publishing to Multi-Marketplaces...")
    marketplace_res = publish_to_marketplaces(zip_path, title)

    # -----------------------------------------------------------
    # Summary
    # -----------------------------------------------------------
    print("\n🎉 JRAVIS PHASE-1 MONETIZATION COMPLETED")
    print("------------------------------------")
    print("Gumroad →", gumroad_res["status"])
    print("Payhip →", payhip_res["status"])
    print("Printify →", printify_res["status"])
    print("Newsletter →", newsletter_res["status"])
    print("Funnel →", funnel_res["status"])
    print("Multi-Marketplace →", marketplace_res["status"])
    print("------------------------------------\n")

    return {
        "gumroad": gumroad_res,
        "payhip": payhip_res,
        "printify": printify_res,
        "newsletter": newsletter_res,
        "funnel": funnel_res,
        "marketplaces": marketplace_res
    }
