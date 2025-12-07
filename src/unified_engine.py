import os
import requests

from publishers.gumroad_publisher import publish_to_gumroad
from publishers.payhip_publisher import publish_to_payhip
from publishers.printify_publisher import publish_to_printify
from publishers.newsletter_publisher import send_newsletter
from publishers.affiliate_funnel_publisher import generate_affiliate_funnel
from publishers.multi_marketplace_publisher import publish_to_marketplaces


def run_all_streams_micro_engine(zip_path: str, title: str, backend_url: str):
    print("\n⚙️ JRAVIS UNIFIED ENGINE")
    print("ZIP =", zip_path)

    # Download ZIP if missing
    if not os.path.exists(zip_path):
        download_url = f"{backend_url}/files/{zip_path.replace('factory_output/','')}"
        print("[DOWNLOAD]", download_url)

        r = requests.get(download_url)
        if r.status_code == 200:
            with open(zip_path, "wb") as f:
                f.write(r.content)
            print("ZIP downloaded")
        else:
            print("[DOWNLOAD ERROR]:", r.text)
            return

    g = publish_to_gumroad(zip_path, title)
    p = publish_to_payhip(zip_path, title)
    pf = publish_to_printify(zip_path, title)
    n = send_newsletter(title)
    f = generate_affiliate_funnel(title)
    m = publish_to_marketplaces(zip_path, title)

    print("\n🎉 MONETIZATION COMPLETE\n")
    return {
        "gumroad": g,
        "payhip": p,
        "printify": pf,
        "newsletter": n,
        "funnel": f,
        "marketplaces": m
    }
