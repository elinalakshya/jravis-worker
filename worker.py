import os
import time
import sys
import requests

SRC = os.path.join(os.getcwd(), "src")
sys.path.append(SRC)

from unified_engine import run_all_streams_micro_engine

BACKEND = os.getenv("BACKEND_URL", "https://jravis-backend.onrender.com")
WORKER_KEY = os.getenv("WORKER_API_KEY")


def api_post(url, data=None):
    try:
        r = requests.post(url, json=data, headers={"X-API-KEY": WORKER_KEY})
        return r.json()
    except:
        return None

def api_get(url):
    try:
        r = requests.get(url, headers={"X-API-KEY": WORKER_KEY})
        return r.json()
    except:
        return None


def run_cycle():
    print("\n🔥 RUNNING JRAVIS CYCLE\n-------------------------------")

    # 1. Generate template
    gen = api_post(f"{BACKEND}/api/factory/generate")
    if not gen or "name" not in gen:
        print("❌ Template generation failed")
        time.sleep(2)
        return

    name = gen["name"]
    zip_path = gen["zip"]
    print("[Factory]", gen)

    # 2. Evaluate growth
    score = api_post(f"{BACKEND}/api/growth/evaluate", {"template": name})
    if not score:
        print("[Growth] FAILED — Using fallback")
        score = {"winner": False}

    # 3. Scale
    print("[Growth]", score)
    api_post(f"{BACKEND}/api/factory/scale/{name}")

    # 4. Monetize
    print("💰 Monetizing...")
    run_all_streams_micro_engine(zip_path, name, BACKEND)


def main():
    print("🚀 JRAVIS WORKER STARTED")

    os.makedirs("factory_output", exist_ok=True)
    os.makedirs("funnels", exist_ok=True)

    while True:
        run_cycle()
        time.sleep(2)


if __name__ == "__main__":
    main()
