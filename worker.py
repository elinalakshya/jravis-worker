# ===============================
# JRAVIS WORKER – STABLE CORE
# ===============================

import os
import sys
import time
import requests

print("🔥 WORKER FILE LOADED")

# -------------------------------
# PATH SETUP (CRITICAL)
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(BASE_DIR, "src")

if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

print("🔧 SRC_PATH =", SRC_PATH)

# ==============================
# FACTORY OUTPUT (CRITICAL)
# ==============================
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

# -------------------------------
# WORKER CYCLE
# -------------------------------
def run_cycle():
    print("\n🔥 RUNNING CYCLE")
    print("--------------------------------")

    # 1️⃣ FACTORY
    task = api_post("/api/factory/generate")
    print("[Factory]", task)

    if not task or task.get("status") != "generated":
        print("❌ Factory failed")
        return

    name = task["name"]

    # 🚨 DO NOT TRUST REMOTE ZIP PATH
    # Always rebuild locally
    local_zip = os.path.join(
        FACTORY_OUTPUT_DIR,
        f"{name}.zip"
    )

    print("📦 EXPECTED ZIP PATH =", local_zip)

    if not os.path.exists(local_zip):
        raise FileNotFoundError(
            f"❌ ZIP NOT FOUND. Factory did not create ZIP: {local_zip}"
        )

    # 2️⃣ GROWTH
    growth = api_post("/api/growth/evaluate")
    print("[Growth]", growth)

    api_post(f"/api/factory/scale/{name}")

    # 3️⃣ MONETIZATION
    print("💰 Monetizing...")
    print(f"⬇️ Using ZIP for {name}")

    print(
        f"🔧 Engine Call: run_all_streams_micro_engine("
        f"'{local_zip}', '{name}', '{BACKEND}')"
    )

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
    print("✅ __main__ TRIGGERED")
    main()
