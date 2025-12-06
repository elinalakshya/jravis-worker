import os

print("📂 Listing deployed directory structure...")
for root, dirs, files in os.walk(".", topdown=True):
    print("DIR:", root)
    for d in dirs:
        print("  📁", d)
    for f in files:
        print("  📄", f)

# -----------------------------------------------------------
# JRAVIS WORKER — Phase-1 Full Automation Engine
# Generates → Evaluates → Scales → Uploads → Promotes
# -----------------------------------------------------------

import os
import sys
import time
import random
import requests
import importlib.util

print("🔧 JRAVIS WORKER INITIALIZING...")


# -----------------------------------------------------------
# AUTO-DETECT ENGINE PATH (jravis-worker/src)
# -----------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENGINE_DIR = os.path.join(BASE_DIR, "jravis-worker", "src")

if os.path.isdir(ENGINE_DIR):
    sys.path.append(ENGINE_DIR)
    print(f"🔧 ENGINE PATH ENABLED → {ENGINE_DIR}")
else:
    print("❌ ERROR: Engine folder not found:", ENGINE_DIR)


# -----------------------------------------------------------
# AUTO-LOAD unified_engine.py (even if name slightly changed)
# -----------------------------------------------------------
engine_file = None

try:
    for f in os.listdir(ENGINE_DIR):
        if f.endswith("_engine.py"):  # catches unified_engine.py
            engine_file = os.path.join(ENGINE_DIR, f)
            print("🔍 ENGINE FILE FOUND →", engine_file)
            break
except Exception as e:
    print("❌ ERROR SCANNING ENGINE FOLDER:", e)

if not engine_file:
    raise FileNotFoundError("❌ ERROR: No *_engine.py file found in jravis-worker/src")

spec = importlib.util.spec_from_file_location("unified_engine", engine_file)
unified_engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(unified_engine)

run_all_streams_micro_engine = unified_engine.run_all_streams_micro_engine
print("✅ Engine Loaded Successfully!")


# -----------------------------------------------------------
# BACKEND API
# -----------------------------------------------------------
BACKEND = os.getenv("BACKEND_URL", "https://jravis-backend.onrender.com")


# ------------------------------------------------------
# Template Generator
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
# Scale Variants
# ------------------------------------------------------
def scale_template(base_name):
    print("[Factory] Scaling:", base_name)
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
# Growth Optimization
# ------------------------------------------------------
def evaluate_growth(template_name):
    try:
        perf = {
            "name": template_name,
            "clicks": random.randint(50, 500),
            "sales": random.randint(0, 20),
            "trend": round(random.uniform(0.8, 1.6), 2)
        }

        r = requests.post(f"{BACKEND}/api/growth/evaluate", json=perf)
        res = r.json()

        print("[Growth] Evaluation:", res)
        return res

    except Exception as e:
        print("[Growth ERROR]:", e)
        return None


# ------------------------------------------------------
# MAIN CYCLE
# ------------------------------------------------------
def run_cycle():
    print("----------------------------------------")
    print("🔥 Running 1 full cycle...")
    print("----------------------------------------")

    # 1. Generate template
    template = generate_template()
    if not template or "name" not in template:
        print("❌ Template generation failed — skipping cycle")
        return

    base_name = template["name"]
    zip_path = template.get("zip")

    # 2. Growth scoring
    growth = evaluate_growth(base_name)

    # 3. Scaling logic
    if growth and growth.get("winner"):
        print("[Growth] WINNER → Scaling aggressively!")
        scale_template(base_name)
        scale_template(base_name)
    else:
        print("[Growth] Normal scaling...")
        scale_template(base_name)

    # 4. Monetization engine
    if zip_path:
        print("\n💰 Triggering Monetization Engine...")
        run_all_streams_micro_engine(zip_path, base_name)
    else:
        print("⚠️ No ZIP found — skipping monetization")


# ------------------------------------------------------
# ENTRY POINT
# ------------------------------------------------------
def main():
    print("🚀 JRAVIS Worker Started — FULL AUTOMATION MODE")

    while True:
        run_cycle()

        # 10-minute heartbeat (100 sec × 6)
        for i in range(6):
            print(f"💓 Heartbeat... ({i+1}/6)")
            time.sleep(100)


if __name__ == "__main__":
    main()
