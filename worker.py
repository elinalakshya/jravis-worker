# -----------------------------------------------------------
# JRAVIS WORKER (FINAL — CLEAN + backend_url FIXED)
# -----------------------------------------------------------

import os
import time
import sys
import requests

# Add /src to import path
SRC_PATH = os.path.join(os.getcwd(), "src")
sys.path.append(SRC_PATH)

print("🔧 SRC PATH =", SRC_PATH)

# Import monetization engine
from unified_engine import run_all_streams_micro_engine

# Backend URL + Worker API Key
BACKEND = os.getenv("BACKEND_URL", "https://jravis-backend.onrender.com")
WORKER_KEY = os.getenv("WORKER_API_KEY")

print("🔧 BACKEND =", BACKEND)


# -----------------------------------------------------------
# API HELPERS
# -----------------------------------------------------------

def get_task():
    url = f"{BACKEND}/api/factory/generate"
    headers = {"X-API-KEY": WORKER_KEY}

    try:
        r = requests.post(url, headers=headers)
        return r.json() if r.status_code == 200 else None
    except Exception as e:
        print("[FACTORY ERROR]", e)
        return None


def scale_task(name):
    url = f"{BACKEND}/api/factory/scale/{name}"
    headers = {"X-API-KEY": WORKER_KEY}

    try:
        r = requests.post(url, headers=headers)
        return r.json()
    except Exception as e:
        print("[SCALE ERROR]", e)
        return None


def evaluate_growth(name):
    url = f"{BACKEND}/api/growth/evaluate/{name}"
    headers = {"X-API-KEY": WORKER_KEY}

    try:
        r = requests.get(url, headers=headers)
        return r.json()
    except Exception as e:
        print("[GROWTH ERROR]", e)
        return None


# -----------------------------------------------------------
# MAIN WORKER CYCLE
# -----------------------------------------------------------

def run_cycle():
    print("\n🔥 RUNNING JRAVIS CYCLE (FINAL)")
    print("--------------------------------------")

    # 1) Generate template
    task = get_task()

    if not task or "name" not in task:
        print("❌ Template generation failed.")
        time.sleep(3)
        return

    name = task["name"]
    zip_path = task["zip"]

    print("[Factory] Response:", task)

    # 2) Growth evaluation
    score = evaluate_growth(name)

    if not score:
        print("❌ Growth evaluation returned None — using default scoring")
        score = {"template": name, "score": 50, "winner": False, "action": "pause"}

    print("[Growth] Evaluation:", score)

    # 3) Scaling logic
    if score.get("winner"):
        print("[Growth] WINNER → DOUBLE SCALE")
        scale_task(name)
        scale_task(name)
    else:
        print("[Growth] Normal Scale")
        scale_task(name)

    # 4) Monetization Engine
    print("💰 Monetizing...")
    print(f"🔧 Calling Engine: run_all_streams_micro_engine('{zip_path}', '{name}', '{BACKEND}')")

    try:
        run_all_streams_micro_engine(zip_path, name, BACKEND)
    except Exception as e:
        print("❌ Monetization Engine ERROR:", e)


# -----------------------------------------------------------
# WORKER LOOP
# -----------------------------------------------------------

def main():
    print("🚀 JRAVIS WORKER STARTED — FINAL MODE")

    os.makedirs("funnels", exist_ok=True)
    os.makedirs("factory_output", exist_ok=True)

    while True:
        run_cycle()
        time.sleep(2)

if __name__ == "__main__":
    main()
