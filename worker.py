# ===========================================================
# JRAVIS WORKER — FULL AUTOMATION ENGINE (Backend + Monetizer)
# Uses Backend API Key: JRAVIS_2040_MASTER_KEY
# ===========================================================

import os
import sys
import time
import random
import requests

# -----------------------------------------------------------
# REQUIRED FOLDERS (Auto-create)
# -----------------------------------------------------------
REQUIRED_FOLDERS = ["funnels", "factory_output"]
for folder in REQUIRED_FOLDERS:
    if not os.path.exists(folder):
        print(f"📁 Creating missing folder: {folder}")
        os.makedirs(folder, exist_ok=True)

# -----------------------------------------------------------
# FIX PYTHON PATH (Render)
# -----------------------------------------------------------
ENGINE_PATH = os.path.join(os.path.dirname(__file__), "src")
sys.path.append(ENGINE_PATH)

try:
    from unified_engine import run_all_streams_micro_engine
    print("🔧 ENGINE LOADED SUCCESSFULLY")
except Exception as e:
    print("❌ ENGINE IMPORT ERROR:", e)
    raise SystemExit


# -----------------------------------------------------------
# API SECURITY (MASTER KEY)
# -----------------------------------------------------------
BACKEND = os.getenv("BACKEND_URL", "https://jravis-backend.onrender.com")

HEADERS = {
    "X-API-KEY": "JRAVIS_2040_MASTER_KEY"
}


# -----------------------------------------------------------
# Factory: Generate Template
# -----------------------------------------------------------
def generate_template():
    print("\n[Factory] Generating template...")
    try:
        r = requests.post(f"{BACKEND}/api/factory/generate", headers=HEADERS)
        return r.json()
    except Exception as e:
        print("[Factory ERROR]:", e)
        return {"error": str(e)}


# -----------------------------------------------------------
# Scaling
# -----------------------------------------------------------
def scale_template(name):
    print(f"[Factory] Scaling {name}")
    try:
        count = random.randint(2, 6)
        r = requests.post(
            f"{BACKEND}/api/factory/scale",
            json={"base": name, "count": count},
            headers=HEADERS
        )
        return r.json()
    except Exception as e:
        print("[Scaling ERROR]:", e)
        return {"error": str(e)}


# -----------------------------------------------------------
# Growth Evaluation
# -----------------------------------------------------------
def evaluate_growth(name):
    try:
        perf = {
            "name": name,
            "clicks": random.randint(50, 400),
            "sales": random.randint(0, 20),
            "trend": round(random.uniform(0.8, 1.6), 2),
        }

        r = requests.post(f"{BACKEND}/api/growth/evaluate", json=perf, headers=HEADERS)
        return r.json()
    except Exception as e:
        print("[Growth ERROR]:", e)
        return {"error": str(e)}


# -----------------------------------------------------------
# FULL EXECUTION CYCLE
# -----------------------------------------------------------
def run_cycle():
    print("\n--------------------------------------")
    print("🔥 RUNNING JRAVIS CYCLE (DEBUG)")
    print("--------------------------------------")

    # 1) Generate
    base = generate_template()
    print("[Factory] Response:", base)

    if "name" not in base:
        print("⚡ Template Name: None")
        return

    name = base["name"]
    zip_path = base.get("zip")

    print(f"⚡ Template Name: {name}")

    # 2) Growth
    growth = evaluate_growth(name)
    print("[Growth] Result:", growth)

    # 3) Scaling
    if growth.get("winner"):
        print("🏆 Winner → Double Scaling!")
        scale_template(name)
        scale_template(name)
    else:
        print("📈 Normal Scaling")
        scale_template(name)

    # 4) Monetization
    if zip_path:
        print("\n💰 Monetization Engine Triggered")
        run_all_streams_micro_engine(zip_path, name)
    else:
        print("⚠️ No ZIP path — skipping monetization")


# -----------------------------------------------------------
# MAIN LOOP
# -----------------------------------------------------------
def main():
    print("🚀 JRAVIS WORKER STARTED — DEBUG + FULL MODE")

    while True:
        run_cycle()
        print("💤 Sleeping 3 seconds...")
        time.sleep(3)


if __name__ == "__main__":
    main()
