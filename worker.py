# =========================================================
# JRAVIS WORKER — PRODUCTION STABLE VERSION
# =========================================================

import os
import sys
import time
import subprocess
import requests

# =========================================================
# GIT FORCE-SYNC (SAFE & IDEMPOTENT)
# =========================================================
def robust_force_sync():
    try:
        print("🔄 JRAVIS worker: starting robust force-sync with GitHub...")
        rc = subprocess.call(
            ["git", "ls-remote", "origin", "HEAD"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        if rc == 0:
            print("🔎 origin found — syncing origin/main")
            subprocess.check_call(["git", "fetch", "origin", "main"])
            subprocess.check_call(["git", "reset", "--hard", "origin/main"])
        else:
            GITHUB_URL = "https://github.com/elinalakshya/jravis-backend.git"
            print("⚠️ origin missing — fetching directly from GitHub")
            subprocess.check_call(["git", "fetch", GITHUB_URL, "main"])
            subprocess.check_call(["git", "reset", "--hard", "FETCH_HEAD"])

        subprocess.call(["git", "config", "--local", "pull.rebase", "false"])
        print("✅ Worker repo synced to GitHub main")

    except Exception as e:
        print("❌ Worker sync failed (continuing):", str(e))


robust_force_sync()
time.sleep(0.3)

# =========================================================
# PATH SETUP
# =========================================================
BASE_DIR = os.getcwd()
SRC_PATH = os.path.join(BASE_DIR, "src")
sys.path.insert(0, SRC_PATH)

print("🔧 SRC_PATH =", SRC_PATH)

# =========================================================
# IMPORT ENGINE
# =========================================================
from unified_engine import run_all_streams_micro_engine

# =========================================================
# BACKEND CONFIG
# =========================================================
BACKEND = os.getenv("BACKEND_URL", "https://jravis-backend.onrender.com")
WORKER_KEY = os.getenv("WORKER_API_KEY")

HEADERS = {"X-API-KEY": WORKER_KEY} if WORKER_KEY else {}

print("🔧 BACKEND =", BACKEND)

# =========================================================
# ZIP DOWNLOAD (✅ FIXED ENDPOINT)
# =========================================================
def download_zip(zip_path: str) -> str:
    """
    Downloads ZIP from backend using secure API endpoint.
    """
    os.makedirs("factory_output", exist_ok=True)

    filename = zip_path.split("/")[-1]
    local_path = os.path.join("factory_output", filename)

    if os.path.isfile(local_path):
        return local_path

    url = f"{BACKEND}/api/factory/download/{filename}"
    print(f"⬇️ Downloading ZIP from {url}")

    r = requests.get(url, headers=HEADERS, stream=True, timeout=60)
    r.raise_for_status()

    with open(local_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    print(f"✅ ZIP downloaded to {local_path}")
    return local_path

# =========================================================
# API HELPERS
# =========================================================
def api_post(path: str):
    try:
        r = requests.post(f"{BACKEND}{path}", headers=HEADERS, timeout=30)
        return r.json() if r.status_code == 200 else None
    except Exception as e:
        print("❌ API POST error:", e)
        return None

# =========================================================
# JRAVIS WORK CYCLE
# =========================================================
def run_cycle():
    print("\n🔥 RUNNING CYCLE")
    print("--------------------------------")

    # -------- FACTORY --------
    task = api_post("/api/factory/generate")

    if not task or task.get("status") != "generated":
        print("❌ Template generation failed")
        print("📦 Factory response:", task)
        time.sleep(5)
        return

    name = task.get("name")
    zip_path = task.get("zip")

    print("[Factory]", task)

    if not name or not zip_path:
        print("❌ Invalid factory payload")
        time.sleep(5)
        return

    # -------- GROWTH --------
    growth = api_post("/api/growth/evaluate")
    print("[Growth]", growth)

    if not growth or "detail" in growth:
        print("⚠️ Growth invalid → Normal scale")
        api_post(f"/api/factory/scale/{name}")
    else:
        if growth.get("winner"):
            print("🏆 WINNER → DOUBLE SCALE")
            api_post(f"/api/factory/scale/{name}")
            api_post(f"/api/factory/scale/{name}")
        else:
            print("➡️ Normal scale")
            api_post(f"/api/factory/scale/{name}")

    # -------- MONETIZE --------
    print("💰 Monetizing...")

    try:
        local_zip = download_zip(zip_path)
        print(
            f"🔧 Engine Call: run_all_streams_micro_engine('{local_zip}', '{name}', '{BACKEND}')"
        )
        run_all_streams_micro_engine(local_zip, name, BACKEND)

    except Exception as e:
        print("❌ Monetization error:", e)

# =========================================================
# MAIN LOOP
# =========================================================
def main():
    print("🚀 JRAVIS WORKER ONLINE")
    os.makedirs("factory_output", exist_ok=True)

    while True:
        try:
            run_cycle()
            time.sleep(2)
        except KeyboardInterrupt:
            print("🛑 Worker stopped manually")
            break
        except Exception as e:
            print("🔥 Worker loop error:", e)
            time.sleep(5)

if __name__ == "__main__":
    main()
