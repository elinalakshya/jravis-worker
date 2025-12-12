# --- JRAVIS: robust auto-sync block (safe, idempotent) ---
import os, time, sys, subprocess

def robust_force_sync():
    try:
        print("🔄 JRAVIS worker: starting robust force-sync with GitHub...")
        # prefer configured origin if valid
        rc = subprocess.call(["git", "ls-remote", "origin", "HEAD"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if rc == 0:
            print("🔎 origin found — fetching origin/main ...")
            subprocess.check_call(["git", "fetch", "origin", "main"])
            subprocess.check_call(["git", "reset", "--hard", "origin/main"])
        else:
            # fallback to direct fetch from GitHub URL
            GITHUB_URL = "https://github.com/elinalakshya/jravis-backend.git"
            print("⚠️ origin missing or not accessible — fetching directly from GitHub URL ...")
            subprocess.check_call(["git", "fetch", GITHUB_URL, "main"])
            subprocess.check_call(["git", "reset", "--hard", "FETCH_HEAD"])

        # ensure git won't stop future pulls with divergent-branch hints
        subprocess.call(["git", "config", "--local", "pull.rebase", "false"])
        print("✅ Worker repo synced to GitHub main (hard reset).")
    except Exception as e:
        print("❌ Worker sync failed (continuing without abort). Error:", str(e))

# Run sync quickly (non-blocking-ish)
robust_force_sync()
time.sleep(0.3)
# --- end sync block ---

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
