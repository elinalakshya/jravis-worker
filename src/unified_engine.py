# -----------------------------------------------------------
# JRAVIS Unified Monetization Engine (FINAL FIX — NO CIRCULAR IMPORT)
# -----------------------------------------------------------

import os
import requests

# Import all publishers directly — NOT unified_engine
from publishers.gumroad_publisher import publish_to_gumroad
from publishers.payhip_publisher import publish_to_payhip
from publishers.printify_publisher import publish_to_printify
from publishers.newsletter_publisher import send_newsletter
from publishers.affiliate_funnel_publisher import generate_affiliate_funnel
from publishers.multi_marketplace_publisher import publish_to_marketplaces


def run_all_streams_micro_engine(zip_path: str, title: str, backend_url: str):
    """
    Full monetization engine with backend ZIP download fallback.
    """

    print("\n⚙️ JRAVIS UNIFIED ENGINE STARTED")
    print("ZIP =", zip_path)
    print("TITLE =", title)

    # --------------------------------------------------
    # ZIP Download (if missing locally)
    # --------------------------------------------------
    if not os.path.exists(zip_path):
        download_url = f"{backend_url}/{zip_path}"
        print(f"[DOWNLOAD] Fetching ZIP: {download_url}")

        r = requests.get(download_url)
        if r.status_code == 200:
            os.makedirs("factory_output", exist_ok=True)
            with open(zip_path, "wb") as f:
                f.write(r.content)
            print("[DOWNLOAD] ZIP saved locally.")
        else:
            print("[DOWNLOAD ERROR]", r.text)
            print("❌ Cannot continue — ZIP missing")
            return None

    # --------------------------------------------------
    # PUBLISHING STREAMS
    # --------------------------------------------------

    gumroad = publish_to_gumroad(zip_path, title)
    payhip = publish_to_payhip(zip_path, title)
    printify = publish_to_printify(zip_path, title)
    newsletter = send_newsletter(title)
    funnel = generate_affiliate_funnel(title)
    marketplaces = publish_to_marketplaces(zip_path, title)

    # --------------------------------------------------
    # SUMMARY
    # --------------------------------------------------
    print("\n🎉 MONETIZATION COMPLETE")
    print("GUMROAD →", gumroad)
    print("PAYHIP →", payhip)
    print("PRINTIFY →", printify)
    print("NEWSLETTER →", newsletter)
    print("FUNNEL →", funnel)
    print("MARKETPLACES →", marketplaces)
    print("--------------------------------------")

    return {
        "gumroad": gumroad,
        "payhip": payhip,
        "printify": printify,
        "newsletter": newsletter,
        "funnel": funnel,
        "marketplaces": marketplaces
    }
