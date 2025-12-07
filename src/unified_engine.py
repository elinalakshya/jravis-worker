# -----------------------------------------------------------
# JRAVIS Unified Monetization Engine (FINAL FIXED VERSION)
# -----------------------------------------------------------

import os
import requests

from publishers.gumroad_publisher import upload_to_gumroad
from publishers.payhip_publisher import upload_to_payhip
from publishers.printify_publisher import upload_to_printify
from publishers.newsletter_content_publisher import send_newsletter
from publishers.affiliate_funnel_publisher import create_affiliate_funnel
from publishers.multi_marketplace_publisher import publish_to_marketplaces

BACKEND = os.getenv("BACKEND_URL", "https://jravis-backend.onrender.com")
API_KEY = os.getenv("WORKER_API_KEY")


# -----------------------------------------------------------
# DOWNLOAD ZIP FROM BACKEND
# -----------------------------------------------------------
def download_zip(zip_path: str):
    file_name = os.path.basename(zip_path)
    local_path = f"factory_output/{file_name}"

    url = f"{BACKEND}/{zip_path}"
    headers = {"X-API-KEY": API_KEY}

    print(f"[DOWNLOAD] Fetching: {url}")

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("[DOWNLOAD ERROR]", r.text)
        return None

    with open(local_path, "wb") as f:
        f.write(r.content)

    print(f"[DOWNLOAD] Saved → {local_path}")
    return local_path


# -----------------------------------------------------------
# CLEAN TITLE
# -----------------------------------------------------------
def extract_title(zip_path: str) -> str:
    base = os.path.basename(zip_path)
    return base.replace(".zip", "").replace("_", " ").title()


# -----------------------------------------------------------
# MASTER MONETIZATION ENGINE
# -----------------------------------------------------------
def run_all_streams_micro_engine(zip_path: str, template_code: str):
    print("\n⚙️ JRAVIS UNIFIED ENGINE STARTED")
    print(f"📦 Input ZIP → {zip_path}")

    # 1. Download real file before uploading
    local_zip = download_zip(zip_path)
    if not local_zip:
        print("❌ ZIP Download Failed — Skipping monetization.")
        return

    title = extract_title(local_zip)
    print(f"📝 Title → {title}")

    # -----------------------------------------------------------
    # 1) Gumroad
    # -----------------------------------------------------------
    print("[GUMROAD] Uploading...")
    gumroad_res = upload_to_gumroad(local_zip, title)

    gumroad_link = gumroad_res.get("url", "https://gumroad.com")

    # -----------------------------------------------------------
    # 2) Payhip
    # -----------------------------------------------------------
    print("[PAYHIP] Uploading...")
    payhip_res = upload_to_payhip(local_zip, title)

    # -----------------------------------------------------------
    # 3) Printify FIXED — include print_areas
    # -----------------------------------------------------------
    print("[PRINTIFY] Creating POD product...")
    printify_res = upload_to_printify(
        local_zip, 
        title,
        print_areas=[{
            "variant_id": 1,
            "placeholders": [{"position": "front", "scale": 1.0}]
        }]
    )

    # -----------------------------------------------------------
    # 4) Newsletter
    # -----------------------------------------------------------
    print("[NEWSLETTER] Sending broadcast...")
    newsletter_res = send_newsletter(title, gumroad_link)

    # -----------------------------------------------------------
    # 5) Funnel
    # -----------------------------------------------------------
    print("[FUNNEL] Creating landing page...")
    funnel_res = create_affiliate_funnel(title, gumroad_link)

    # -----------------------------------------------------------
    # 6) Marketplaces
    # -----------------------------------------------------------
    print("[MARKETPLACES] Publishing...")
    marketplace_res = publish_to_marketplaces(local_zip, title)

    print("\n🎉 MONETIZATION COMPLETE\n")

    return {
        "gumroad": gumroad_res,
        "payhip": payhip_res,
        "printify": printify_res,
        "newsletter": newsletter_res,
        "funnel": funnel_res,
        "marketplaces": marketplace_res,
    }
