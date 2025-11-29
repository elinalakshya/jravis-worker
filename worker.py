import time
import requests
from settings import (
    BACKEND_URL,
    PRINTIFY_API_KEY,
    MESHY_API_KEY,
    GUMROAD_TOKEN,
    PAYHIP_API_KEY,
    OPENAI_API_KEY
)

from publisher_printify import publish_printify_product
from publisher_payhip import publish_payhip_product
from publisher_gumroad import publish_gumroad_product
from publisher_meshy import generate_meshy_assets


def fetch_task():
    try:
        r = requests.get(f"{BACKEND_URL}/task/next")
        return r.json()
    except Exception as e:
        print("❌ Error fetching task:", e)
        return {"status": "error"}


def mark_done(task_id):
    try:
        requests.post(f"{BACKEND_URL}/task/done/{task_id}")
        print(f"✔ Marked task as done: {task_id}")
    except:
        print("⚠ Could not mark task done")


def run_worker():
    print("🚀 JRAVIS Worker Started — Waiting for tasks…")

    while True:
        task = fetch_task()

        if task.get("status") == "empty":
            time.sleep(2)
            continue

        if "task" not in task:
            time.sleep(1)
            continue

        t = task["task"]
        print(f"📥 Received Task: {t}")

        try:
            if t["type"] == "printify_pod":
                publish_printify_product(PRINTIFY_API_KEY)

            elif t["type"] == "payhip_upload":
                publish_payhip_product(PAYHIP_API_KEY)

            elif t["type"] == "gumroad_upload":
                publish_gumroad_product(GUMROAD_TOKEN)

            elif t["type"] == "meshy_assets":
                generate_meshy_assets(MESHY_API_KEY)

            else:
                print("⚠ Unknown task type:", t["type"])

        except Exception as e:
            print("❌ Worker processing error:", e)

        mark_done(task["id"])
        time.sleep(1)


if __name__ == "__main__":
    run_worker()
