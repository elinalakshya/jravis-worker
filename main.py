# -----------------------------------------------------------
# JRAVIS BRAIN v3 — MASTER CONTROLLER
# Ethical + Legal + Original + Human-like + Robo Speed
# Controls all JRAVIS services from ONE FILE.
# -----------------------------------------------------------

import requests
import random
import time
import hashlib

# -----------------------------------------------------------
# SERVICE URLS (Replace with your live deployments)
# -----------------------------------------------------------
BACKEND = "https://jravis-backend.onrender.com"
INTELLIGENCE = "https://jravis-intelligence-worker.onrender.com"
MEMORY = "https://jravis-memory-worker.onrender.com"
REPORT = "https://jravis-report-service.onrender.com"

LOCK = "JRV2040_LOCKED_KEY_001"


# -----------------------------------------------------------
# UNIQUE CONTENT GENERATOR (no reuse, no plagiarism)
# -----------------------------------------------------------
def generate_unique_content():
    topics = [
        "wealth creation", "ai automation", "global business", "mindset",
        "productivity", "ethical income", "mission 2040 growth",
        "digital freedom"
    ]

    topic = random.choice(topics)

    # Generate original idea
    idea = f"New insight on {topic}: Focus on {random.choice(['consistency', 'quality', 'long-term value', 'automation', 'customer trust'])} to grow faster."

    # Add uniqueness using hashed randomness
    unique_stamp = hashlib.sha256(str(
        random.random()).encode()).hexdigest()[:12]

    content = f"{idea}\n#{topic.replace(' ', '')}_{unique_stamp}"

    return content


# -----------------------------------------------------------
# HUMAN MODE — Safe, slow, real human behaviour
# -----------------------------------------------------------
def human_mode():
    actions = [
        "scrolling feed", "reading a post", "liking content",
        "commenting politely", "saving a post", "checking notifications"
    ]

    action = random.choice(actions)
    delay = round(random.uniform(2.5, 8.0), 2)

    return {"mode": "human", "action": action, "delay": delay}


# -----------------------------------------------------------
# ROBO MODE — Fast content creation engine
# -----------------------------------------------------------
def robo_mode():
    return {
        "mode": "robo",
        "action": "create_content",
        "content": generate_unique_content(),
        "count": random.randint(2, 5)
    }


# -----------------------------------------------------------
# BRAIN DECISION — 60% Robo, 40% Human for safety
# -----------------------------------------------------------
def brain_decision():
    if random.random() <= 0.60:
        return robo_mode()
    else:
        return human_mode()


# -----------------------------------------------------------
# SEND TASK TO BACKEND QUEUE
# -----------------------------------------------------------
def queue_task(task):
    return requests.post(f"{BACKEND}/task/new",
                         json={
                             "task": task,
                             "lock": LOCK
                         }).json()


# -----------------------------------------------------------
# TRIGGER OTHER SERVICES
# -----------------------------------------------------------
def run_intelligence():
    return requests.get(f"{INTELLIGENCE}/run").json()


def run_memory():
    return requests.get(f"{MEMORY}/sync").json()


def run_reports():
    return requests.get(f"{REPORT}/generate").json()


# -----------------------------------------------------------
# MAIN LOOP — Runs every hour
# -----------------------------------------------------------
def main():
    while True:
        print("\n🔥 JRAVIS-BRAIN v3 — STARTING CYCLE")

        # 1. Make a decision
        task = brain_decision()
        print("🧠 Decision:", task)

        # 2. Queue the task
        backend = queue_task(task)
        print("📥 Task Queue:", backend)

        # 3. Run intelligence worker (posting + human behaviour)
        intel = run_intelligence()
        print("🤖 Intelligence Worker:", intel)

        # 4. Update memory so no duplicates ever happen
        mem = run_memory()
        print("💾 Memory Sync:", mem)

        # 5. Generate daily/weekly reports
        rep = run_reports()
        print("📊 Reports:", rep)

        print("⏳ Sleeping 1 hour…\n")
        time.sleep(3600)


if __name__ == "__main__":
    main()
