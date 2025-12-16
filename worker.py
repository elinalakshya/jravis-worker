# ===============================
# JRAVIS WORKER – STEP 4 FINAL
# ===============================

import os
import sys
import time
import requests

print("🚨 WORKER VERSION = STEP4-FINAL-NAME-ONLY")

# -------------------------------
# PATH SETUP
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(BASE_DIR, "src")

if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

print("🔧 SRC_PATH =", SRC_PATH)

# -------------------------------
# FACTORY OUTPUT DIR
# -------------------------------
FACTORY_OUTPUT_DIR = os.path.join(BASE_DIR, "factory_output")
os.makedirs(FACTORY_OUTPUT_DIR, exist_ok=True)

print("📁 FACTORY_OUTPUT_DIR =", FACTORY_OUTPUT_DIR)

# -------------------------------
# BACKEND CONFIG
# -------------------------------
BACKEND = os.getenv(
    "BACKEND_URL",
    "https://jravis-backend.onrender.com"
).rstrip("/")

WORKER_KEY = os.getenv("WORKER_API_KEY")

HEADERS = {}
if WORKER_KEY:
    HEADERS["X-API-KEY"] = WORKER_KEY

print("🔧 BACKEND =", BACKEND)

# -------------------------------
# IMPORT ENGINE
# -------------------------------
try:
    from unified_engine import run_all_streams_micro_engine
    print("✅ unified_engine imported")
except Exception as e:
    print("❌ Failed to import unified_engine:", e)
    sys.exit(1)

# -------------------------------
# API HELPERS
# -------------------------------
def api_post(path: str):
    url = f"{BACKEND}{path}"
    return requests.post(url, headers=HEADERS, timeout=60).json()


def download_zip(name: str, local_zip_path: str):
    """
    Downloads ZIP using backend API:
    GET /api/factory/download/{name}
    """
    url = f"{BACKEND}/api/factory/download/{name}"
    print(f"⬇️ Downloading ZIP from API: {url}")

    with requests.get(url, headers=HEADERS, stream=True, timeout=120) as r:
        r.raise_for_status()
        with open(local_zip_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    print(f"✅ ZIP downloaded to: {local_zip_path}")

# -------------------------------
# WORKER CYCLE
# -------------------------------
def run_cycle():
    print("\n🔥 RUNNING CYCLE")
    print("--------------------------------")

    # 1️⃣ FACTORY GENERATE
    task = api_post("/api/factory/generate")
    print("[Factory]", task)

    if not task or task.get("status") != "generated":
        print("❌ Factory failed")
        return

    name = task["name"]

    local_zip = os.path.join(
        FACTORY_OUTPUT_DIR,
        f"{name}.zip"
    )

    print("📦 TEMPLATE NAME =", name)
    print("📦 LOCAL ZIP =", local_zip)

    # 2️⃣ DOWNLOAD ZIP (API ONLY)
    download_zip(name, local_zip)

    if not os.path.exists(local_zip):
        raise FileNotFoundError(f"ZIP missing after download: {local_zip}")

    # 3️⃣ GROWTH
    growth = api_post("/api/growth/evaluate")
    print("[Growth]", growth)

    api_post(f"/api/factory/scale/{name}")

    # 4️⃣ MONETIZATION
    print("💰 Monetizing...")
    run_all_streams_micro_engine(
        local_zip,
        name,
        BACKEND
    )

# -------------------------------
# MAIN LOOP
# -------------------------------
def main():
    print("🚀 JRAVIS WORKER ONLINE")

    while True:
        try:
            run_cycle()
            print("💓 HEARTBEAT OK")
            time.sleep(5)
        except Exception as e:
            print("🔥 Worker loop error:", e)
            time.sleep(5)

# -------------------------------
# ENTRYPOINT
# -------------------------------
if __name__ == "__main__":
    main()
