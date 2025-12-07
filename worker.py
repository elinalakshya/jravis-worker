# -----------------------------------------------------------
# JRAVIS WORKER — FINAL VERSION (PATH FIXED)
# -----------------------------------------------------------

import os
import sys
import time
import random
import requests

# ------------------------------
# FIX PYTHON PATH FOR RENDER
# ------------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(CURRENT_DIR, "src")

if SRC_DIR not in sys.path:
    print("🔧 Adding SRC path:", SRC_DIR)
    sys.path.append(SRC_DIR)

# ------------------------------
# IMPORT ENGINE
# ------------------------------
from unified_engine import run_all_streams_micro_engine


# BACKEND URL
BACKEND = os.getenv("BACKEND_URL", "https://jravis-backend.onrender.com")
API_KEY = os.getenv("WORKER_API_KEY")


# ------------------------------
# Generate Template
# ------------------------------
def generate_template():
    print("\n[Factory] Generating template...")

    try:
        res = requests.post(
            f"{BACKEND}/api/factory/generate",
            headers={"X-API-KEY": API_KEY}
        ).json()
        print("[Factory] Response:", res)
        return res
    except Exception as e:
        print("[Factory ERROR]", e)
        return None


# ------------------------------
# Scale Template
# ------------------------------
def scale_template(base):
    try:
        count = random.randint(2, 6)
        res = requests.post(
            f"{BACKEND}/api/factory/scale",
            headers={"X-API-KEY": API_KEY},
            json={"base": base, "count": count}
        ).json()
        print("[Scale] Response:", res)
        return res
    except Exception as e:
        print("[Scale ERROR]", e)
        return None


# ------------------------------
# Growth Evaluation
# ------------------------------
def evaluate_growth(name):
    data = {
        "template": name,
        "clicks": random.randint(50, 500),
        "sales": random.randint(0, 20),
        "score": random.uniform(10, 200)
    }

    try:
        res = requests.post(
            f"{BACKEND}/api/growth/evaluate",
            headers={"X-API-KEY": API_KEY},
            json=data
        ).json()
        print("[Growth]", res)
        return res
    except Exception as e:
        print("[Growth ERROR]", e)
        return None


# ------------------------------
# FULL CYCLE
# ------------------------------
def run_cycle():
    print("\n🔥 RUNNING JRAVIS CYCLE (DEBUG)")
    print("--------------------------------------")

    tpl = generate_template()
    if not tpl or "name" not in tpl:
        print("⚠ Template generation failed.")
        return

    name = tpl["name"]
    zip_path = tpl["zip"]

    growth = evaluate_growth(name)

    if growth.get("winner"):
        print("[WINNER] Double scaling")
        scale_template(name)
        scale_template(name)
    else:
        print("[NORMAL] Single scaling")
        scale_template(name)

    print("💰 Monetizing...")
    run_all_streams_micro_engine(zip_path, name)


# ------------------------------
# MAIN LOOP
# ------------------------------
def main():
    print("🚀 JRAVIS WORKER STARTED")

    while True:
        run_cycle()
        time.sleep(3)


if __name__ == "__main__":
    main()
