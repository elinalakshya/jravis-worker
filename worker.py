# =========================================================
# JRAVIS WORKER — STREAMING GENERATE (PRODUCTION FINAL)
# =========================================================

import os
import sys
import time
import subprocess
import requests
import traceback

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
            subprocess.check_call(["git", "fetch", "origin", "main"])
            subprocess.check_call(["git", "reset", "--hard", "origin/main"])
        else:
            GITHUB_URL = "https://github.com/elinalakshya/jravis-backend.git"
            subprocess.check_call(["git", "fetch", GITHUB_URL, "main"])
            subprocess.check_call(["git", "reset", "--hard", "FETCH_HEAD"])

        subprocess.call(["git", "config", "--local", "pull.rebase", "false"])
        print("✅ Worker repo synced to GitHub main")
    except Exception as e:
        print("❌ Worker sync failed (continuing):", e)

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
# API HELPERS
# =========================================================
def api_post(path):
    try:
        r = requests.post(
            f"{BACKEND}{path}",
            headers=HEADERS,
            timeout=30,
        )
        return r.json() if r.status_code == 200 else None
    except Exception as e:
        print("❌ API POST error:", e)
        return None

# =========================================================
# STREAMING ZIP GENERATION
# =========================================================
def stream_generate_zip(template_name: str) -> str:
    """
    Streams ZIP directly from backend and saves locally.
    """
    os.makedirs("factory_output", exist_ok=True)
    local_zip = os.path.join("factory_output", f"{template_name}.zip")

    headers = {
        **HEADERS,
        "X-Template-Name": template_name,
    }

    print(f"⬇️ Streaming ZIP for {template_name}...")

    with requests.post(
        f"{BACKEND}/api/factory/generate",
        headers=headers,
        stream=True,
        timeout=180,
    ) as r:
        r.raise_for_status()
        with open(local_zip, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    print(f"✅ ZIP saved: {local_zip}")
    return local_zip

# =========================================================
# JRAVIS CYCLE
# =========================================================
def run_cycle():
    print("\n🔥 RUNNING CYCLE")
    print("--------------------------------")

    # -------- FACTORY META --------
    task = api_post("/api/factory/generate")
    if not task or task.get("status") != "generated":
        print("❌ Template generation failed:", task)
        time.sleep(5)
        return

    name = task["name"]
    print("[Factory]", task)

    # -------- GROWTH --------
    growth = api_post("/api/growth/evaluate")
    print("[Growth]", growth)

    if growth and growth.get("winner"):
        print("🏆 WINNER → DOUBLE SCALE")
        api_post(f"/api/factory/scale/{name}")
        api_post(f"/api/factory/scale/{name}")
    else:
        print("➡️ Normal scale")
        api_post(f"/api/factory/scale/{name}")

    # -------- MONETIZE --------
    try:
        print("💰 Monetizing...")
        local_zip = stream_generate_zip(name)

        print(
            f"🔧 Engine Call: run_all_streams_micro_engine('{local_zip}', '{name}', '{BACKEND}')"
        )

        run_all_streams_micro_engine(local_zip, name, BACKEND)

    except Exception:
        print("❌ Monetization error:")
        print(traceback.format_exc())

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
        except Exception:
            print("🔥 Worker loop error:")
            print(traceback.format_exc())
            time.sleep(5)

if __name__ == "__main__":
    main()
