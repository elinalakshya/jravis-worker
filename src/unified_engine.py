# -----------------------------------------------------------
# JRAVIS Unified Monetization Engine (FINAL VERSION)
# Downloads ZIP → Uploads to all platforms → Generates funnels
# -----------------------------------------------------------

import os
import requests

from publishers.gumroad_publisher import upload_to_gumroad
from publishers.payhip_publisher import upload_to_payhip
from publishers.printify_publisher import upload_to_printify
from publishers.newsletter_content_publisher import send_newsletter
from publishers.affiliate_funnel_publisher import create_affiliate_funnel
from publishers.multi_marketplace_publisher import publish_to_marketplaces


BACKEND_URL = os.getenv("BACKEND_URL", "https://jravis-backend.onrender.com")


# -----------------------------------------------------------
# DOWNLOAD ZIP FROM BACKEND
# -----------------------------------------------------------
def download_zip(zip_path: str) -> str:
    """
    JRAVIS Backend returns ZIP paths like:
        factory_output/template-1234.zip

    Worker must download:
        https://jravis-backend.onrender.com/factory_output/template-1234.zip
    """

    url = f"{BACKEND_URL}/{zip_path}"
    local_file = f"/tmp/{os.path.basename(zip_path)}"

    print(f"[DOWNLOAD] Fetching: {url}")

    try:
        r = requests.get(url, timeout=20)
        if r.status_code != 200:
            print("[DOWNLOAD ERROR]", r.text)
            return None

        with open(local_file, "wb") as f:
            f.write(r.content)

        print(f"[DOWNLOAD] Saved → {local_file}")
        return local_file

    except Exception as e:
        print("[DOWNLOAD ERROR]", e)
        return None


# -----------------------------------------------------------
# Extract Title from ZIP
# -----------------------------------------------------------
def extract_title(zip_path: str) -> str:
    base = os.path.basename(zip_path)
    name = base.replace(".zip", "").replace("_", " ").title()
    return name


# -----------------------------------------------------------
# Main Unified Engine
# -----------------------------------------------------------
def run_all_streams_micro_engine(zip_path: str, template_name: str):
    print("\n⚙️ JRAVIS UNIFIED ENGINE STARTED")
    print("📦 Input ZIP →", zip_path)

    # 1. Download actual ZIP file from backend
    local_zip = download_zip(zip_path)
    if not local_zip:
        print("❌ ZIP Download Failed — Skipping monetization.")
        return

    title = extract_title(zip_path)
    print("📝 Title →", title)

    # -------------------------------------------------------
    # 2. Gumroad Upload
    # -------------------------------------------------------
    print("\n[GUMROAD] Uploading", title, "...")
    gumroad_res = upload_to_gumroad(local_zip, title)

    gumroad_link = None
    try:
        gumroad_link = gumroad_res["response"]["product"]["short_url"]
    except:
        gumroad_link = "https://gumroad.com"

    # -------------------------------------------------------
    # 3. Payhip Upload
    # -------------------------------------------------------
    print("\n[PAYHIP] Uploading", title, "...")
    payhip_res = upload_to_payhip(local_zip, title)

    # -------------------------------------------------------
    # 4. Printify Upload
    # -------------------------------------------------------
    print("\n[PRINTIFY] Uploading POD asset for", title, "...")
    printify_res = upload_to_printify(local_zip, title)

    # -------------------------------------------------------
    # 5. Newsletter Blast
    # -------------------------------------------------------
    print("\n[NEWSLETTER] Sending broadcast for", title, "...")
    newsletter_res = send_newsletter(title, gumroad_link)

    # -------------------------------------------------------
    # 6. Funnel Generation
    # -------------------------------------------------------
    print("\n[FUNNEL] Creating affiliate funnel for", title, "...")
    funnel_res = create_affiliate_funnel(title, gumroad_link)

    # -------------------------------------------------------
    # 7. Multi-Marketplace
    # -------------------------------------------------------
    print("\n[MARKETPLACES] Publishing", title, "to external networks...")
    marketplace_res = publish_to_marketplaces(local_zip, title)

    # -------------------------------------------------------
    # Summary Log
    # -------------------------------------------------------
    print("\n🎉 MONETIZATION COMPLETE")
    print("--------------------------------------")
    print("Gumroad →", gumroad_res.get("status"))
    print("Payhip →", payhip_res.get("status"))
    print("Printify →", printify_res.get("status"))
    print("Newsletter →", newsletter_res.get("status"))
    print("Funnel →", funnel_res.get("status"))
    print("Marketplaces →", marketplace_res.get("status"))
    print("--------------------------------------\n")

    return {
        "gumroad": gumroad_res,
        "payhip": payhip_res,
        "printify": printify_res,
        "newsletter": newsletter_res,
        "funnel": funnel_res,
        "marketplaces": marketplace_res
    }
