# =========================================================
# JRAVIS WORKER — STREAMING GENERATE (FINAL)
# =========================================================

import os
import sys
import time
import requests

BASE_DIR = os.getcwd()
SRC_PATH = os.path.join(BASE_DIR, "src")
sys.path.insert(0, SRC_PATH)

from unified_engine import run_all_streams_micro_engine

BACKEND = os.getenv("BACKEND_URL", "https://jravis-backend.onrender.com")
WORKER_KEY = os.getenv("WORKER_API_KEY")

HEADERS = {}
if WORKER_KEY:
    HEADERS["X-API-KEY"] = WORKER_KEY

os.makedirs("factory_output", exist_ok=True)

def run_cycle():
    print("\n🔥 RUNNING CYCLE")
    print("--------------------------------")

    # 🔥 STREAM ZIP DIRECTLY (NO DOWNLOAD API)
    r = requests.post(
        f"{BACKEND}/api/factory/generate",
        headers=HEADERS,
        timeout=60,
    )

    r.raise_for_status()

    template_name = r.headers.get("X-Template-Name")
    if not template_name:
        raise RuntimeError("Missing X-Template-Name header")

    local_zip = f"factory_output/{template_name}.zip"

    with open(local_zip, "wb") as f:
        f.write(r.content)

    print(f"✅ ZIP STREAMED: {local_zip}")

    # 💰 MONETIZE
    run_all_streams_micro_engine(
        local_zip,
        template_name,
        BACKEND
    )

def main():
    print("🚀 JRAVIS WORKER ONLINE (STREAM MODE)")

    while True:
        try:
            run_cycle()
            time.sleep(2)
        except KeyboardInterrupt:
            print("🛑 Worker stopped")
            break
        except Exception as e:
            print("❌ Worker error:", e)
            time.sleep(5)

if __name__ == "__main__":
    main()
