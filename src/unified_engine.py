import os
import hashlib
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from publishers.gumroad_engine import run_gumroad_engine

BASE_DIR = "factory_output"
STATE_FILE = os.path.join(BASE_DIR, ".jravis_state.json")

os.makedirs(BASE_DIR, exist_ok=True)

# -------------------------------
# STATE (IDEMPOTENCY)
# -------------------------------
def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

# -------------------------------
# UTILS
# -------------------------------
def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def run_with_retry(fn, label, retries=3):
    for i in range(retries):
        try:
            return fn()
        except Exception as e:
            print(f"⚠️ [{label}] attempt {i+1}/{retries} failed:", e)
            time.sleep(2)
    raise RuntimeError(f"{label} failed after retries")

# -------------------------------
# ENGINE (ZIP ONLY)
# -------------------------------
def run_all_streams_micro_engine(zip_path, template_name, backend_url=None):
    print(f"🚀 unified_engine START for {template_name}")

    if not os.path.isfile(zip_path):
        raise RuntimeError(f"ZIP path is not a file: {zip_path}")

    state = load_state()
    zip_hash = sha256(zip_path)

    if zip_hash not in state:
        state[zip_hash] = {}

    publishers = {
        "gumroad": lambda: run_gumroad_engine(zip_path, template_name),
    }

    results = {}

    with ThreadPoolExecutor(max_workers=len(publishers)) as pool:
        futures = {}

        for name, fn in publishers.items():
            if state[zip_hash].get(name):
                print(f"⏭️ {name} already completed, skipping")
                continue
            futures[pool.submit(run_with_retry, fn, name)] = name

        for future in as_completed(futures):
            name = futures[future]
            future.result()
            state[zip_hash][name] = True
            results[name] = "success"

    save_state(state)
    print("📊 ENGINE COMPLETE:", results)
