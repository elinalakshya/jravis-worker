# ===========================================================
# JRAVIS UNIFIED MONETIZATION ENGINE
# Gumroad + Payhip + Printify + Newsletter + Funnel
# ===========================================================

import os

from publishers.gumroad_publisher import upload_to_gumroad
from publishers.payhip_publisher import upload_to_payhip
from publishers.printify_publisher import upload_to_printify
from publishers.newsletter_content_publisher import send_newsletter
from publishers.affiliate_funnel_publisher import create_affiliate_funnel
from publishers.multi_marketplace_publisher import publish_to_marketplaces


# -----------------------------------------------------------
# Extract Title from ZIP
# -----------------------------------------------------------
def extract_title(zip_path):
    base = os.path.basename(zip_path)
    return base.replace(".zip", "").replace("_", " ").title()


# -----------------------------------------------------------
# MAIN ENGINE
# -----------------------------------------------------------
def run_all_streams_micro_engine(zip_path, template_code):
    print("\n⚙️ JRAVIS Unified Monetization Engine Booting...")
    print(f"📦 ZIP: {zip_path}")

    title = extract_title(zip_path)
    print(f"📝 Title Generated: {title}")

    # 1) Gumroad
    print("\n🚀 Publishing to Gumroad...")
    gumroad_res = upload_to_gumroad(zip_path, title)

    try:
        gumroad_link = gumroad_res["response"]["product"]["short_url"]
    except:
        gumroad_link = "https://gumroad.com"

    # 2) Payhip
    print("\n🚀 Publishing to Payhip...")
    payhip_res = upload_to_payhip(zip_path, title)

    # 3) Printify
    print("\n👕 Creating Printify Product...")
    printify_res = upload_to_printify(zip_path, title)

    # 4) Newsletter
    print("\n📧 Sending Newsletter...")
    newsletter_res = send_newsletter(title, gumroad_link)

    # 5) Funnels
    print("\n🌀 Generating Funnel Page...")
    funnel_res = create_affiliate_funnel(title, gumroad_link)

    # 6) Multi-Marketplace
    print("\n🌍 Publishing to Multi-Marketplaces...")
    marketplace_res = publish_to_marketplaces(zip_path, title)

    print("\n🎉 PHASE-1 MONETIZATION COMPLETED\n")
    return {
        "gumroad": gumroad_res,
        "payhip": payhip_res,
        "printify": printify_res,
        "newsletter": newsletter_res,
        "funnel": funnel_res,
        "marketplaces": marketplace_res,
    }
