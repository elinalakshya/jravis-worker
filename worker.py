import os
import time
import requests
from pathlib import Path

from src.unified_engine import run_all_streams_micro_engine

BACKEND = os.getenv("BACKEND_URL")
API_KEY = os.getenv("WORKER_API_KEY")

if not BACKEND:
    raise RuntimeError("BACKEND_URL is missing")

HEADERS = {"X-API-KEY": API_KEY}

os.makedirs("factory_output", exist_ok=True)
os.makedirs("funnels", exist_ok=True)


def download_zip(zip_path):
    """Download ZIP from backend / factory_output route"""
    url = f"{BACKEND}/{zip_path}"
    print(f"[DOWNLOAD] GET → {url}")

    r = requests.get(url, headers=HEADERS)

    if r.status_code != 200:
        print("[DOWNLOAD ERROR]", r.text)
        return None

    # Ensure directory exists
    Path(zip_path).parent.mkdir(parents=True, exist_ok=True)

    with open(zip_path, "wb") as f:
        f.write(r.content)

    return zip_path


def run_cycle():
    print("--------------------------------------")
    print("🔥 RUNNING JRAVIS CYCLE")

    # Step 1 — Generate template
    res = requests.post(f"{BACKEND}/factory/generate", headers=HEADERS).json()
    print("[FACTORY]", res)

    if "zip" not in res:
        print("❌ No ZIP returned, skipping.")
        return

    name = res["name"]
    zip_path = res["zip"]

    # Step 2 — Download ZIP
    local_zip = download_zip(zip_path)
    if not local_zip:
        print("❌ ZIP download failed")
        return

    # Step 3 — Monetization
    run_all_streams_micro_engine(local_zip, name)


if __name__ == "__main__":
    print("🚀 JRAVIS WORKER STARTED")
    while True:
        run_cycle()
        time.sleep(5)
