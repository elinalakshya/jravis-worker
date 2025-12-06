# -----------------------------------------------------------
# JRAVIS WORKER — Batch 9 & Batch 11 Unified Worker Engine
# -----------------------------------------------------------

import os
import time
import random
import requests

BACKEND = os.getenv("BACKEND_URL", "https://jravis-backend.onrender.com")


# -----------------------------------------------------------
# Batch 9 — Template Generator
# -----------------------------------------------------------
def generate_template():
    print("\n[Factory] Generating new template...")
    try:
        r = requests.post(f"{BACKEND}/api/factory/generate")
        return r.json()
    except Exception as e:
        print("[Factory] ERROR:", e)
        return None


def scale_template(base_name):
    print("[Factory] Scaling template:", base_name)
    try:
        count = random.randint(2, 6)
        r = requests.post(
            f"{BACKEND}/api/factory/scale",
            json={"base": base_name, "count": count}
        )
        return r.json()
    except Exception as e:
        print("[Factory] Scale ERROR:", e)
        return None


# -----------------------------------------------------------
# Batch 11 — Pricing AI
# -----------------------------------------------------------
def send_pricing_request(name):
    print("[Pricing] Calculating price for:", name)
    try:
        r = requests.post(
            f"{BACKEND}/api/pricing/calc",
            json={
                "name": name,
                "complexity": round(random.uniform(0.9, 1.5), 2),
                "trending": round(random.uniform(0.8, 1.4), 2)
            }
        )
        print("[Pricing Response]:", r.json())
        return r.json()
    except Exception as e:
        print("[Pricing ERROR]:", e)
        return None


# -----------------------------------------------------------
# Worker Loop
# -----------------------------------------------------------
def main():
    print("🚀 JRAVIS Worker Started — Batch 9 & 11 Active")

    while True:

        # 45% probability of generating a new template
        if random.random() < 0.45:
            t = generate_template()

            if t and "name" in t:
                base = t["name"]

                # Scale variants
                scale_template(base)

                # Pricing AI will price this template
                send_pricing_request(base)

        # System still runs pricing for at least 1 template every cycle
        send_pricing_request("auto-pricing-template")

        print("⏳ Sleeping 10 minutes...\n")
        time.sleep(600)


if __name__ == "__main__":
    main()
