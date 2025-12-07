# -----------------------------------------------------------
# AUTO-CREATE REQUIRED DIRECTORIES
# -----------------------------------------------------------

import os

REQUIRED_FOLDERS = ["funnels", "factory_output", "publishers", "src"]

for folder in REQUIRED_FOLDERS:
    if not os.path.exists(folder):
        print(f"📁 Creating missing folder: {folder}")
        os.makedirs(folder, exist_ok=True)

# -----------------------------------------------------------
# JRAVIS WORKER — FULL AUTOMATION MODE
# Template Creation → Growth Evaluation → Scaling → Monetization
# -----------------------------------------------------------

import os
import time
import random
import requests

# ENGINE IMPORT (works correctly now)
from unified_engine import run_all_streams_micro_engine


# BACKEND URL
BACKEND = os.getenv("BACKEND_URL", "https://jravis-backend.onrender.com")


# ------------------------------------------------------
# 1) Generate Template ZIP
# ------------------------------------------------------
def generate_template():
    print("\n[Factory] Generating new template...")
    try:
        res = requests.post(f"{BACKEND}/api/factory/generate").json()
        print("[Factory] Generated:", res)
        return res
    except Exception as e:
        print("[Factory] ERROR generating:", e)
        return None


# ------------------------------------------------------
# 2) Scale Template Variants
# ------------------------------------------------------
def scale_template(base_name):
    print(f"[Factory] Scaling: {base_name}")
    try:
        count = random.randint(2, 6)
        res = requests.post(
            f"{BACKEND}/api/factory/scale",
            json={"base": base_name, "count": count}
        ).json()
        print("[Factory] Scaled:", res)
        return res
    except Exception as e:
        print("[Factory] ERROR scaling:", e)
        return None


# ------------------------------------------------------
# 3) Growth Engine — Score Winners
# ------------------------------------------------------
def evaluate_growth(template_name):
    try:
        perf = {
            "name": template_name,
            "clicks": random.randint(50, 500),
            "sales": random.randint(0, 20),
            "trend": round(random.uniform(0.8, 1.6), 2),
        }

        r = requests.post(f"{BACKEND}/api/growth/evaluate", json=perf)
        res = r.json()

        print("[Growth] Evaluation:", res)
        return res

    except Exception as e:
        print("[Growth ERROR]:", e)
        return None


# ------------------------------------------------------
# 4) FULL CYCLE
# ------------------------------------------------------
def run_cycle():
    print("\n----------------------------------------")
    print("🔥 RUNNING FULL JRAVIS CYCLE")
    print("----------------------------------------")

    # STEP 1 — Generate Template
    template = generate_template()
    if not template or "name" not in template:
        print("❌ Template generation failed — Skipping")
        return

    base_name = template["name"]
    zip_path = template.get("zip")

    # STEP 2 — Growth Scoring
    growth = evaluate_growth(base_name)

    # STEP 3 — Scaling
    if growth and growth.get("winner"):
        print("[Growth] WINNER — Double Scaling Mode Activated!")
        scale_template(base_name)
        scale_template(base_name)  # Double scaling for winners
    else:
        print("[Growth] Normal scaling")
        scale_template(base_name)

    # STEP 4 — Monetization Engine
    if zip_path:
        print("\n💰 Starting Monetization Engine...")
        run_all_streams_micro_engine(zip_path, base_name)
    else:
        print("⚠️ No ZIP found — Monetization Skipped")


# ------------------------------------------------------
# 5) ENTRY POINT — MAIN LOOP
# ------------------------------------------------------
def main():
    print("🚀 JRAVIS WORKER STARTED — FULL AUTOMATION ENABLED")

    while True:
        run_cycle()

        # Heartbeat every 10 minutes (100s × 6 = 600s)
        for i in range(6):
            print(f"💓 Heartbeat ({i+1}/6)")
            time.sleep(100)


# ------------------------------------------------------
if __name__ == "__main__":
    main()
