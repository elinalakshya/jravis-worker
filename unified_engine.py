import os
import zipfile
import hashlib
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from publishers.gumroad_engine import run_gumroad_engine
# add others later

BASE_OUTPUT = "factory_output"
EXTRACT_DIR = os.path.join(BASE_OUTPUT, "extracted")
PUBLISH_DIR = os.path.join(BASE_OUTPUT, "publish_ready")
STATE_FILE = os.path.join(BASE_OUTPUT, ".jravis_state.json")

os.makedirs(EXTRACT_DIR, exist_ok=True)
os.makedirs(PUBLISH_DIR, exist_ok=True)

# -------------------------------
# STATE (STEP 5.3 PREP)
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

def extract_zip(zip_path, out_dir):
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(out_dir)

def zip_folder(folder_path, out_zip):
    with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(folder_path):
            for file in files:
                full = os.path.join(root, file)
                arc = os.path.relpath(full, folder_path)
                z.write(full, arc)

# -------------------------------
# RETRY
# -------------------------------
def run_with_retry(fn, label, retries=3):
    for i in range(retries):
        try:
            return fn()
        except Exception as e:
            print(f"⚠️ [{label}] attempt {i+1}/{retries} failed:", e)
            time.sleep(2)
    raise RuntimeError(f"{label} failed after retries")

# -------------------------------
# ENGINE
# -------------------------------
def run_all_streams_micro_engine(zip_path, template_name, backend_url=None):
    print(f"🚀 unified_engine START for {template_name}")

    state = load_state()
    zip_hash = sha256(zip_path)

    if zip_hash not in state:
        state[zip_hash] = {}

    # -------------------------------
    # EXTRACT
    # -------------------------------
    extract_path = os.path.join(EXTRACT_DIR, template_name)
    os.makedirs(extract_path, exist_ok=True)

    extract_zip(zip_path, extract_path)
    print("📂 ZIP extracted to", extract_path)

    # -------------------------------
    # RE-ZIP FOR PUBLISHING
    # -------------------------------
    publish_zip = os.path.join(PUBLISH_DIR, f"{template_name}.zip")
    zip_folder(extract_path, publish_zip)
    print("📦 Publish-ready ZIP =", publish_zip)

    # -------------------------------
    # PUBLISHERS (PARALLEL SAFE)
    # -------------------------------
    publishers = {
        "gumroad": lambda: run_gumroad_engine(publish_zip, template_name),
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
