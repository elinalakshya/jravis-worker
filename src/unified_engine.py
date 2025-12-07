# -----------------------------------------------------------
# JRAVIS WORKER (FINAL VERSION)
# -----------------------------------------------------------

import os
import sys
import time
import random
import requests

# Ensure correct path for unified_engine
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")
sys.path.insert(0, SRC_DIR)

from unified_engine import run_all_streams_micro_engine


BACKEND = os.getenv("BACKEND_URL", "https://jravis-backend.onrender.com")


def generate_template():
    print("[Factory] Generating template...")
    try:
        res = requests.post(f"{BACKEND}/api/factory/generate").json()
        print("[Factory] Response:", res)
        return res
    except Exception as e:
        print("[Factory ERROR]", e)
        return None


def scale_template(name):
    print("[Factory] Scaling:", name)
    try:
        count = random.randint(2, 6)
        res = requests.post(
            f"{BACKEND}/api/factory/scale",
            json={"base": name, "count": count}
        ).json()
        print("[Factory] Scaled:", res)
        return res
    except Exception as e:
        print("[SCALE ERROR]", e)
        return None


def evaluate_growth(name):
    score = {
        "template": name,
        "clicks": random.randint(50, 500),
        "sales": random.randint(0, 20),
        "trend": round(random.uniform(0.8, 1.6), 3)
    }

    try:
        res = requests.post(f"{BACKEND}/api/growth/evaluate", json=score).json()
        print("[Growth] Evaluation:", res)
        return res
    except Exception as e:
        print("[Growth ERROR]", e)
        return None


def run_cycle():
    print("\n--------------------------------------")
    print("🔥 RUNNING JRAVIS CYCLE (FINAL)")
    print("--------------------------------------")

    # STEP 1 — Generate Template
    tpl = generate_template()
    if not tpl or "name" not in tpl:
        print("❌ Template generation failed.")
        return

    name = tpl["name"]
    zip_path = tpl["zip"]

    # STEP 2 — Growth Check
    growth = evaluate_growth(name)
    if growth and growth.get("winner"):
        print("[Growth] WINNER → DOUBLE SCALE")
        scale_template(name)
        scale_template(name)
    else:
        print("[Growth] Normal Scale")
        scale_template(name)

    # STEP 3 — Monetization
    print("💰 Monetizing...")

    try:
        run_all_streams_micro_engine(zip_path, name, BACKEND)  
        # <-- FIXED: 3 arguments
    except Exception as e:
        print("❌ Monetization Engine ERROR:", e)


def main():
    print("🚀 JRAVIS WORKER STARTED — FINAL MODE")
    os.makedirs("factory_output", exist_ok=True)
    os.makedirs("funnels", exist_ok=True)

    while True:
        run_cycle()
        time.sleep(3)


if __name__ == "__main__":
    main()
