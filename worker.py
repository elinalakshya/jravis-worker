# -----------------------------------------------------------
# JRAVIS WORKER — Autonomous Execution Engine
# Handles Streams, Intelligence, Memory, Factory, n8n Sync
# -----------------------------------------------------------

import time
import requests
import random
import hashlib
import os

BACKEND = os.getenv("BACKEND_URL", "https://jravis-backend.onrender.com")
N8N_WEBHOOK = os.getenv("N8N_WEBHOOK_URL", "")
N8N_SECRET = os.getenv("N8N_WEBHOOK_SECRET", "")

LOCK = os.getenv("JRAVIS_LOCK", "JRV2040_LOCKED_KEY_001")


# -----------------------------------------------------------
# SAFE UNIQUE CONTENT GENERATOR
# -----------------------------------------------------------
def generate_unique_content():
    topics = [
        "automation", "digital wealth", "scaling", "templates",
        "funnels", "ai growth", "mindset", "mission2040",
    ]

    topic = random.choice(topics)
    base = f"Insight on {topic}: Focus on consistency, automation and clean scaling."

    stamp = hashlib.sha256(str(random.random()).encode()).hexdigest()[:12]
    return f"{base}\n#{topic}_{stamp}"


# -----------------------------------------------------------
# TASK DECISION ENGINE (human + robo safe)
# -----------------------------------------------------------
def human_mode():
    actions = ["scroll", "read", "like", "save", "observe"]
    return {"mode": "human", "action": random.choice(actions), "delay": random.uniform(2, 6)}


def robo_mode():
    return {
        "mode": "robo",
        "action": "create_content",
        "count": random.randint(2, 4),
        "content": generate_unique_content(),
    }


def brain_decision():
    return robo_mode() if random.random() < 0.65 else human_mode()


# -----------------------------------------------------------
# BACKEND TASK QUEUE
# -----------------------------------------------------------
def queue_task(task):
    try:
        r = requests.post(f"{BACKEND}/api/task/new",
                          json={"task": task, "lock": LOCK},
                          timeout=20)
        return r.json()
    except:
        return None


# -----------------------------------------------------------
# Intelligence Worker Trigger
# -----------------------------------------------------------
def run_intelligence():
    try:
        r = requests.get(f"{BACKEND}/api/intelligence/run", timeout=20)
        return r.json()
    except:
        return None


# -----------------------------------------------------------
# Batch 9 — Factory Engine Trigger
# -----------------------------------------------------------
def run_factory():
    try:
        r = requests.get(f"{BACKEND}/api/factory/generate", timeout=20)
        return r.json()
    except:
        return None


# -----------------------------------------------------------
# Sync to n8n Factory Webhook (optional, safe mode)
# -----------------------------------------------------------
def push_to_n8n(payload):
    if not N8N_WEBHOOK:
        return None

    payload["secret"] = N8N_SECRET

    try:
        r = requests.post(N8N_WEBHOOK, json=payload, timeout=20)
        return r.status_code
    except:
        return None


# -----------------------------------------------------------
# MAIN WORKER LOOP
# -----------------------------------------------------------
def main():
    print("[JRAVIS] Worker Booting...")

    while True:
        print("\n============================")
        print("🔥 JRAVIS WORKER — NEW CYCLE")
        print("============================")

        # 1. Brain Decision
        task = brain_decision()
        print("🧠 Decision:", task)

        # 2. Send to Backend
        q = queue_task(task)
        print("📥 Task Queue Result:", q)

        # 3. Intelligence Worker
        intel = run_intelligence()
        print("🤖 Intelligence Worker:", intel)

        # 4. Factory System (Batch 9)
        factory = run_factory()
        print("🏭 Factory Output:", factory)

        # 5. Sync to n8n
        if factory:
            print("🔗 Syncing Factory Batch to n8n...")
            push_to_n8n(factory)

        print("⏳ Sleeping 60 seconds…")
        time.sleep(60)  # (You selected every 1 minute)

if __name__ == "__main__":
    main()
