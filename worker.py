# ===============================
# JRAVIS WORKER – STREAM ZIP SAFE
# ===============================

import os
import sys
import time
import uuid
import requests

print("🚨 WORKER VERSION = STREAM-ZIP-VALIDATED")

# -------------------------------
# PATH SETUP
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(BASE_DIR, "src")

if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

print("🔧 SRC_PATH =", SRC_PATH)

# -------------------------------
# OUTPUT DIR
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
# ZIP VALIDATION
# -------------------------------
def is_valid_zip(path):
    try:
        with open(path, "rb") as f:
            signature = f.read(4)
            return signature == b"PK\x03\x04"
    except Exception:
        return False

# -------------------------------
# WORKER CYCLE
# -------------------------------
def run_cycle():
    print("\n🔥 RUNNING CYCLE")
    print("--------------------------------")

    resp = requests.post(
        f"{BACKEND}/api/factory/generate",
        headers=HEADERS,
        stream=True,
        timeout=120
    )

    resp.raise_for_status()

    content_type = resp.headers.get("Content-Type", "")
    print("📨 RESPONSE Content-Type =", content_type)

    template_name = f"template-{uuid.uuid4().hex[:6]}"
    local_zip = os.path.join(FACTORY_OUTPUT_DIR, f"{template_name}.zip")

    print("📦 TEMPLATE NAME =", template_name)
    print("📦 SAVING ZIP TO =", local_zip)

    with open(local_zip, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    if not os.path.exists(local_zip):
        print("❌ ZIP file missing after save")
        return

    # -------------------------------
    # ZIP VALIDATION GATE
    # -------------------------------
    if not is_valid_zip(local_zip):
        print("❌ INVALID ZIP FILE RECEIVED")
        print("⚠️ Skipping this cycle safely")

        # Debug: show first bytes
        with open(local_zip, "rb") as f:
            preview = f.read(200)
            print("🧪 FILE PREVIEW:", preview)

        return

    print("✅ ZIP VALIDATED")

    # -------------------------------
    # RUN UNIFIED ENGINE
    # -------------------------------
    run_all_streams_micro_engine(
        local_zip,
        template_name,
    )

# -------------------------------
# MAIN LOOP
# -------------------------------
def main():
    print("🚀 JRAVIS WORKER ONLINE (STREAM ZIP SAFE)")

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
