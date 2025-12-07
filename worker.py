# -----------------------------------------------------------
# JRAVIS WORKER (FINAL — backend_url FIXED)
# -----------------------------------------------------------

import os
import time
import sys
import requests

sys.path.append(os.path.join(os.getcwd(), "src"))

from unified_engine import run_all_streams_micro_engine


BACKEND = os.getenv("BACKEND_URL", "https://jravis-backend.onrender.com")


def get_task():
    """Fetch new template from backend factory."""
    url = f"{BACKEND}/api/factory/generate"
    headers = {"X-API-KEY": os.getenv("WORKER_API_KEY")}
    try:
        r = requests.post(url, headers=headers)
        if r.status_code == 200:
            return r.json()
        return None
    except Exception as e:
        print("[TASK ERROR]", e)
        return None


def scale_task(name):
    """Ask backend to scale the template."""
    url = f"{BACKEND}/api/factory/scale/{name}"
    headers = {"X-API-KEY": os.getenv("WORKER_API_KEY")}
    try:
        r = requests.post(url, headers=headers)
        if r.status_code == 200:
            return r.json()
        return None
    except Exception as e:
        print("[SCALE ERROR]", e)
        return None


def evaluate_growth(name):
    """Ask backend growth engine to evaluate template."""
    url = f"{BACKEND}/api/growth/evaluate/{name}"
    headers = {"X-API-KEY": os.getenv("WORKER_API_KEY")}
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return r.json()
        return None
    except Exception as e:
        print("[GROWTH ERROR]", e)
        return None


def run_cycle():
    print("🔥 RUNNING JRAVIS CYCLE (FINAL)")
    print("--------------------------------------")

    task = get_task()
    if not task or "name" not in task:
        print("❌ Template generation failed.")
        time.sleep(3)
        return

    name = task["name"]
    zip_path = task["zip"]

    print("[Factory] Response:", task)

    # Growth Evaluation
    score = evaluate_growth(name)
    if not score:
        print("❌ Growth evaluation failed.")
        return

    print("[Growth] Evaluation:", score)

    winner = score.get("winner", False)

    # Scale if winner
    if winner:
        print("[Growth] WINNER → DOUBLE SCALE")
        scale_task(name)
        scale_task(name)
    else:
        print("[Growth] Normal Scale")
        scale_task(name)

    # Now MONETIZE
    print("💰 Monetizing...")

    # FIXED → 3 arguments
    try:
        run_all_streams_micro_engine(zip_path, name, BACKEND)
    except Exception as e:
        print("❌ Monetization Engine ERROR:", e)


def main():
    print("🚀 JRAVIS WORKER STARTED — FINAL MODE")

    while True:
        run_cycle()
        time.sleep(2)


if __name__ == "__main__":
    os.makedirs("funnels", exist_ok=True)
    os.makedirs("factory_output", exist_ok=True)

    # Ensure src path is added
    src_path = os.path.join(os.getcwd(), "src")
    sys.path.append(src_path)

    print("🔧 Adding SRC path:", src_path)

    main()
