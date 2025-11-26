# JRAVIS MEMORY SYNC WORKER
# Mission 2040 — Duplicate Protection & Task Memory Engine

import requests
import time
import json
import os

BACKEND = os.getenv("BACKEND_URL", "https://jravis-backend.onrender.com")
MEMORY_FILE = "memory_store.json"


# ------------------------------------------------------
# Load & Save Memory
# ------------------------------------------------------
def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


# ------------------------------------------------------
# Check if content already exists
# ------------------------------------------------------
def is_duplicate(task, memory):
    task_content = json.dumps(task["task"], sort_keys=True)
    for entry in memory:
        if entry == task_content:
            return True
    return False


# ------------------------------------------------------
# Worker Loop
# ------------------------------------------------------
def main():
    print("🔥 JRAVIS MEMORY WORKER — Started")

    memory = load_memory()

    while True:
        try:
            # Fetch next task
            resp = requests.get(f"{BACKEND}/task/next", timeout=20)
            data = resp.json()

            # No tasks
            if data.get("status") == "empty":
                print("⏳ No tasks. Waiting...")
                time.sleep(5)
                continue

            task_id = data["id"]
            task_info = data

            # Check duplicates
            if is_duplicate(task_info, memory):
                print("⚠️ Duplicate detected — marking task completed")
                requests.post(f"{BACKEND}/task/done/{task_id}")
                continue

            # Add to memory
            memory.append(json.dumps(task_info["task"], sort_keys=True))
            save_memory(memory)

            print(f"✅ NEW TASK STORED IN MEMORY — {task_id}")

            # Mark task done
            requests.post(f"{BACKEND}/task/done/{task_id}")

        except Exception as e:
            print("❌ ERROR:", e)

        time.sleep(2)


if __name__ == "__main__":
    main()
