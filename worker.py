# worker.py

import os
import sys
import time
import requests
import subprocess

# =========================================================
# CONFIG
# =========================================================
BACKEND = os.getenv("BACKEND_URL", "https://jravis-backend.onrender.com")
WORKER_KEY = os.getenv("WORKER_API_KEY", "")
HEADERS = {"X-API-KEY": WORKER_KEY} if WORKER_KEY else {}

BASE_DIR = os.getcwd()
SRC_PATH = os.path.join(BASE_DIR, "src")
os.makedirs("factory_output", exist_ok=True)

sys.path.insert(0, SRC_PATH)

print("🔧 BACKEND =", BACKEND)
print("🔧 SRC_PATH =", SRC_PATH)

# =========================================================
# IMPORT ENGINE
# =========================================================
from unified_engine import run_all_streams_micro_engine

# =========================================================
# API HELPERS
# =========================================================
def api_post(path: str):
    r = requests.post(f"{BACKEND}{path}", headers=HEADERS, timeout=60)
    r.raise_for_status()
    return r.json()

def stream_zip(template_name: str) -> str:
    """
    Streams ZIP directly from backend (Solution #1)
    """
    url = f"{BACKEND}/api/factory/stream"
    headers = {"X-Template-Name": template_name}

    local_path = f"factory_output/{template_name}.zip"

    print(f"⬇️ Streaming ZIP for {template_name}...")

    with requests.get(url, headers=headers, stream=True, timeout=120) as r:
        r.raise_for_status()
        with open(local_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    print(f"✅ ZIP saved: {local_path}")
    return local_path

# =========================================================
# MAIN LOOP
# =========================================================
def run_cycle():
    print("\n🔥 RUNNING CYCLE")
    print("--------------------------------")

    # -------- FACTORY --------
    task = api_post("/api/factory/generate")
    print("[Factory]", task)

    if task.get("status") != "generated":
        print("❌ Factory failed")
        return

    name = task["name"]

    # -------- GROWTH --------
    growth = api_post("/api/growth/evaluate")
    print("[Growth]", growth)

    api_post(f"/api/factory/scale/{name}")

    # -------- MONETIZE --------
    try:
        zip_path = stream_zip(name)
        print(f"🔧 Engine Call: run_all_streams_micro_engine('{zip_path}', '{name}', '{BACKEND}')")
        run_all_streams_micro_engine(zip_path, name, BACKEND)
    except Exception as e:
        print("❌ Monetization error:", e)

def main():
    print("🚀 JRAVIS WORKER ONLINE")
    while True:
        try:
            run_cycle()
            time.sleep(2)
        except KeyboardInterrupt:
            print("🛑 Worker stopped")
            break
        except Exception as e:
            print("🔥 Worker loop error:", e)
            time.sleep(5)

if __name__ == "__main__":
    main()
