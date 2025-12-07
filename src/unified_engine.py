import os
from publishers.gumroad_publisher import upload_to_gumroad
from publishers.payhip_publisher import upload_to_payhip
from publishers.printify_publisher import upload_to_printify
from publishers.newsletter_content_publisher import send_newsletter
from publishers.affiliate_funnel_publisher import create_affiliate_funnel
from publishers.multi_marketplace_publisher import publish_to_marketplaces

def extract_title(zip_path):
    base = os.path.basename(zip_path)
    return base.replace(".zip", "").replace("_", " ").title()

def run_all_streams_micro_engine(zip_path, code):
    title = extract_title(zip_path)

    print("\n⚙️ JRAVIS UNIFIED ENGINE STARTED")
    print(f"📦 Input ZIP → {zip_path}")
    print(f"📝 Title → {title}")

    gumroad = upload_to_gumroad(zip_path, title)
    payhip = upload_to_payhip(zip_path, title)
    printify = upload_to_printify(zip_path, title)
    newsletter = send_newsletter(title, gumroad.get("url", ""))
    funnel = create_affiliate_funnel(title, gumroad.get("url", ""))
    markets = publish_to_marketplaces(zip_path, title)

    print("\n🎉 MONETIZATION COMPLETE\n")

    return {
        "gumroad": gumroad,
        "payhip": payhip,
        "printify": printify,
        "newsletter": newsletter,
        "funnel": funnel,
        "markets": markets
    }
