# -----------------------------------------------------------
# JRAVIS WORKER — FULL AUTOMATION ENGINE (FIXED VERSION)
# Factory → Growth → Scaling → Monetization
# -----------------------------------------------------------

import os
import sys
import time
import random
import requests

# -----------------------------------------------------------
# AUTO-CREATE REQUIRED DIRECTORIES
# -----------------------------------------------------------
REQUIRED_FOLDERS = ["funnels", "factory_output", "publishers", "src"]
for folder in REQUIRED_FOLDERS:
    if not os.path.exists(folder):
        print(f"📁 Creating missing folder: {folder}")
        os.makedirs(folder, exist_ok=True)

# -----------------------------------------------------------
# FIX PYTHON PATH FOR RENDER
# -----------------------------------------------------------
ENGINE_PATH = os.path.join(os.path.dirname(__file__), "src")
if ENGINE_PATH not in sys.path:
    print("🔧 Adding engine path:", ENGINE_PATH)
    sys.path.append(ENGINE_PATH)

# IMPORT ENGINE
from unified_engine import run_all_streams_micro_engine


# -----------------------------------------------------------
# CONFIG VARIABLES
# -----------------------------------------------------------
BACKEND = os.getenv("BACKEND_URL", "https://jravis-backend.onrender.com")
WORKER_KEY = os.getenv("WORKER_API_KEY", "NO_KEY_SET")

HEADERS = {"X-API-KEY": WORKER_KEY}


# -----------------------------------------------------------
# 1) Generate Template ZIP
# -----------------------------------------------------------
def generate_template():
    print("\n[Factory] Generating new template...")
    try:
        res = requests.post(f"{BACKEND}/factory/generate", headers=HEADERS)
        data = res.json()
        print("[Factory] Response:", data)
        return data
    except Exception as e:
        print("[Factory] ERROR:", e)
        return None


# -----------------------------------------------------------
# 2) Scale Template Variants
# -----------------------------------------------------------
def scale_template(base_name):
    print(f"[Factory] Scaling template: {base_name}")
    try:
        count = random.randint(2, 6)

        res = requests.post(
            f"{BACKEND}/factory/scale",
            json={"base": base_name, "count": count},
            headers=HEADERS
        )

        data = res.json()
        print("[Factory] Scale Response:", data)
        return data

    except Exception as e:
        print("[Factory] ERROR scaling:", e)
        return None


# -----------------------------------------------------------
# 3) Growth Evaluation
# -----------------------------------------------------------
def evaluate_growth(template_name):
    print("[Growth] Evaluating performance...")

    perf = {
        "name": template_name,
        "clicks": random.randint(50, 500),
        "sales": random.randint(0, 20),
        "trend": round(random.uniform(0.8, 1.6), 2),
    }

    try:
        r = requests.post(
            f"{BACKEND}/growth/evaluate",
            json=perf,
            headers=HEADERS
        )
        data = r.json()
        print("[Growth] Response:", data)
        return data
    except Exception as e:
        print("[Growth ERROR]:", e)
        return None


# -----------------------------------------------------------
# 4) FULL CYCLE EXECUTION
# -----------------------------------------------------------
def run_cycle():
    print("\n--------------------------------------")
    print("🔥 RUNNING JRAVIS CYCLE")
    print("--------------------------------------")

    # Step 1 — GENERATE TEMPLATE
    template = generate_template()
    if not template or "name" not in template:
        print("❌ Failed to generate template — retrying next cycle")
        return

    base_name = template["name"]
    zip_path = template.get("zip")

    # Step 2 — GROWTH SCORING
    growth = evaluate_growth(base_name)

    # Step 3 — SCALING
    if growth and growth.get("winner"):
        print("[Growth] WINNER → Double scaling mode!")
        scale_template(base_name)
        scale_template(base_name)
    else:
        print("[Growth] Normal scaling...")
        scale_template(base_name)

    # Step 4 — MONETIZATION ENGINE
    if zip_path:
        print("\n💰 Running Monetization Engine...")
        run_all_streams_micro_engine(zip_path, base_name)
    else:
        print("⚠️ No ZIP found → monetization skipped")


# -----------------------------------------------------------
# MAIN LOOP
# -----------------------------------------------------------
def main():
    print("🚀 JRAVIS WORKER STARTED — FULL AUTO MODE")

    while True:
        run_cycle()

        # Heartbeat every 10 minutes
        for i in range(6):
            print(f"💓 Heartbeat ({i+1}/6)")
            time.sleep(100)


if __name__ == "__main__":
    main()
