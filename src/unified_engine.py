# -----------------------------------------------------------
# JRAVIS UNIFIED MICRO-ENGINE
# Runs all monetization streams for 1 template zip
# -----------------------------------------------------------

import os
import json
import time
from publishers.gumroad_publisher import upload_to_gumroad
from publishers.payhip_publisher import upload_to_payhip
from publishers.printify_publisher import send_to_printify
from publishers.newsletter_publisher import send_newsletter
from publishers.affiliate_funnel_publisher import build_funnel_page


def run_all_streams_micro_engine(zip_path, product_name):
    print("\n==============================")
    print("🧠 JRAVIS Monetization Engine")
    print("==============================")

    metadata = {
        "name": product_name,
        "price": 12,
        "file": zip_path
    }

    # -----------------------------
    # 1. Gumroad
    # -----------------------------
    print("\n[ENGINE] 🚀 Uploading to Gumroad...")
    try:
        gum = upload_to_gumroad(metadata)
        print("[ENGINE] Gumroad →", gum)
    except Exception as e:
        print("[ENGINE] ❌ Gumroad Error:", e)

    # -----------------------------
    # 2. Payhip
    # -----------------------------
    print("[ENGINE] 🚀 Uploading to Payhip...")
    try:
        pay = upload_to_payhip(metadata)
        print("[ENGINE] Payhip →", pay)
    except Exception as e:
        print("[ENGINE] ❌ Payhip Error:", e)

    # -----------------------------
    # 3. Printify
    # -----------------------------
    print("[ENGINE] 👕 Sending artwork to Printify...")
    try:
        pr = send_to_printify(metadata)
        print("[ENGINE] Printify →", pr)
    except Exception as e:
        print("[ENGINE] ❌ Printify Error:", e)

    # -----------------------------
    # 4. Newsletter Blast
    # -----------------------------
    print("[ENGINE] 📧 Sending Newsletter Blast...")
    try:
        nw = send_newsletter(metadata)
        print("[ENGINE] Newsletter →", nw)
    except Exception as e:
        print("[ENGINE] ⚠️ Newsletter Error:", e)

    # -----------------------------
    # 5. Affiliate Funnel Page
    # -----------------------------
    print("[ENGINE] 🌀 Creating Affiliate Funnel...")
    try:
        fn = build_funnel_page(metadata)
        print("[ENGINE] Funnel Saved →", fn)
    except Exception as e:
        print("[ENGINE] ⚠️ Funnel Error:", e)

    print("\n🎯 Monetization Cycle Completed\n")
    return True
