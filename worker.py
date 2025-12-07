import os
import time
import random
import requests
import sys

# Add SRC path
ROOT = os.path.dirname(__file__)
if ROOT not in sys.path:
    sys.path.append(ROOT)

# Import monetization engine
from unified_engine import run_all_streams_micro_engine

BACKEND = os.getenv("BACKEND_URL", "https://jravis-backend.onrender.com")
WORKER_KEY = os.getenv("WORKER_API_KEY")


def generate_template():
    print("\n[Factory] Generating template...")
    try:
        r = requests.post(
            f"{BACKEND}/factory/generate",
            headers={"X-API-KEY": WORKER_KEY}
        )
        print("[Factory] Response:", r.json())
        return r.json()
    except Exception as e:
        print("[Factory] ERROR:", e)
        return None


def scale_template(base):
    try:
        count = random.randint(2, 5)
        r = requests.post(
            f"{BACKEND}/factory/scale",
            json={"base": base, "count": count},
            headers={"X-API-KEY": WORKER_KEY}
        )
        print("[Factory] Scaled:", r.json())
        return r.json()
    except Exception as e:
        print("[Scale ERROR]", e)
        return None


def evaluate_growth(name):
    try:
        payload = {
            "name": name,
            "clicks": random.randint(50, 500),
            "sales": random.randint(0, 30),
            "trend": round(random.uniform(0.8, 1.6), 2)
        }
        r = requests.post(
            f"{BACKEND}/api/growth/evaluate",
            json=payload,
            headers={"X-API-KEY": WORKER_KEY}
        )
        res = r.json()
        print("[Growth] Evaluation:", res)
        return res
    except Exception as e:
        print("[Growth ERROR]", e)
        return None


def run_cycle():
    print("\n--------------------------------------")
    print("🔥 RUNNING JRAVIS CYCLE")
    print("--------------------------------------")

    t = generate_template()
    if not t or "name" not in t:
        print("❌ Template generation failed")
        time.sleep(3)
        return

    name = t["name"]
    zip_path = t["zip"]

    growth = evaluate_growth(name)

    if growth and growth.get("winner"):
        print("[Growth] WINNER → DOUBLE SCALE")
        scale_template(name)
        scale_template(name)
    else:
        print("[Growth] Normal scale")
        scale_template(name)

    print("💰 Monetizing...")
    run_all_streams_micro_engine(zip_path, name)


if __name__ == "__main__":
    print("🚀 JRAVIS WORKER ACTIVE")
    while True:
        run_cycle()
        time.sleep(5)
