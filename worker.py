# -----------------------------------------------------------
# JRAVIS WORKER — Batch 9 Auto-Scaling Factory Engine
# Generates templates + scales variants every 10 minutes
# -----------------------------------------------------------

import os
import time
import random
import requests


BACKEND = os.getenv("BACKEND_URL", "https://jravis-backend.onrender.com")


# ------------------------------------------------------
# 1️⃣ New Template Generator (POST + JSON BODY REQUIRED)
# ------------------------------------------------------
def generate_template():
    print("\n[Factory] Generating new template...")

    payload = {
        "template_name": f"auto_template_{int(time.time())}"
    }

    try:
        res = requests.post(
            f"{BACKEND}/api/factory/generate",
            json=payload,     # << REQUIRED
            timeout=30
        ).json()

        print("[Factory] Generated:", res)
        return res

    except Exception as e:
        print("[Factory] ERROR generating:", e)
        return None


# ------------------------------------------------------
# 2️⃣ Scale Variants
# ------------------------------------------------------
def scale_template(base_name):
    print("[Factory] Scaling template:", base_name)

    try:
        count = random.randint(2, 6)

        res = requests.post(
            f"{BACKEND}/api/factory/scale",
            json={"base": base_name, "count": count},
            timeout=30
        ).json()

        print("[Factory] Scaled Variants:", res)
        return res

    except Exception as e:
        print("[Factory] ERROR scaling:", e)
        return None


# ------------------------------------------------------
# 3️⃣ Worker Loop
# ------------------------------------------------------
def main():
    print("🚀 JRAVIS Factory Worker Started (Batch 9 Active)")

    while True:

        # Generate approximately every 20–30 minutes
        if random.random() < 0.45:
            template = generate_template()

            if template and "name" in template:
                base = template["name"]

                # Auto-scale variants
                scale_template(base)

        print("⏳ Sleeping 10 minutes...\n")
        time.sleep(600)


# ------------------------------------------------------
# Entry Point
# ------------------------------------------------------
if __name__ == "__main__":
    main()
