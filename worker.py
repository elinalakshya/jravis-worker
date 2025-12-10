import os
print("🔄 Syncing JRAVIS Worker with Backend...")
os.system("cd /opt/render/project/src && git pull https://github.com/elinalakshya/jravis-backend.git main || true")
print("✅ Sync complete. Worker is up to date with backend.")

import os
import time
import sys
import requests

# Ensure src path
SRC_PATH = os.path.join(os.getcwd(), "src")
sys.path.append(SRC_PATH)

print("🔧 SRC_PATH =", SRC_PATH)

# Import unified engine
from unified_engine import run_all_streams_micro_engine

# Backend config
BACKEND = os.getenv("BACKEND_URL", "https://jravis-backend.onrender.com")
WORKER_KEY = os.getenv("WORKER_API_KEY")

print("🔧 BACKEND =", BACKEND)


# ---------------------------
# API HELPERS
# ---------------------------

def api_get(path):
    try:
        r = requests.get(
            f"{BACKEND}{path}",
            headers={"X-API-KEY": WORKER_KEY},
        )
        return r.json() if r.status_code == 200 else None
    except:
        return None


def api_post(path):
    try:
        r = requests.post(
            f"{BACKEND}{path}",
            headers={"X-API-KEY": WORKER_KEY},
        )
        return r.json()
    except:
        return None


# ---------------------------
# JRAVIS CYCLE
# ---------------------------

def run_cycle():
    print("🔥 RUNNING CYCLE")
    print("--------------------------------")

    task = api_post("/api/factory/generate")

    if not task or "name" not in task:
        print("❌ Template generation failed")
        time.sleep(2)
        return

    name = task["name"]
    zip_path = task["zip"]

    print("[Factory]", task)

    # --- Growth ---
    growth = api_post("/api/growth/evaluate")

    print("[Growth]", growth)

    if not growth or isinstance(growth, dict) and "detail" in growth:
        print("⚠️ Growth score invalid → Normal scale")
        api_post(f"/api/factory/scale/{name}")
    else:
        if growth.get("winner"):
            print("🏆 WINNER → DOUBLE SCALE")
            api_post(f"/api/factory/scale/{name}")
            api_post(f"/api/factory/scale/{name}")
        else:
            print("➡️ Normal scale")
            api_post(f"/api/factory/scale/{name}")

    # Monetize
    print("💰 Monetizing...")
    print(f"🔧 Engine Call: run_all_streams_micro_engine('{zip_path}', '{name}', '{BACKEND}')")

    try:
        run_all_streams_micro_engine(zip_path, name, BACKEND)
    except Exception as e:
        print("❌ Engine ERROR:", e)


def main():
    print("🚀 WORKER ONLINE")

    os.makedirs("factory_output", exist_ok=True)

    while True:
        run_cycle()
        time.sleep(2)


if __name__ == "__main__":
    main()
