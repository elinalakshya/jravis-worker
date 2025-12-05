# -----------------------------------------------------------
# JRAVIS BRAIN v4 — MASTER CONTROLLER (Mission 2040)
# Ethical + Legal + Human-like + Robo Fast + Intelligence Mode
# -----------------------------------------------------------

import requests
import random
import time
import hashlib

# -----------------------------------------------------------
# SERVICE URLS (LIVE DEPLOYMENTS)
# -----------------------------------------------------------
BACKEND = "https://jravis-backend.onrender.com"
INTEL = "https://jravis-intelligence-worker.onrender.com"
MEMORY = "https://jravis-memory-worker.onrender.com"
REPORT = "https://jravis-report-service.onrender.com"

LOCK = "JRV2040_LOCKED_KEY_001"

# -----------------------------------------------------------
# INTELLIGENCE MODE (Boss chose: AGGRESSIVE)
# -----------------------------------------------------------
INTELLIGENCE_MODE = "aggressive"   # conservative | balanced | aggressive


# -----------------------------------------------------------
# UNIQUE CONTENT GENERATOR — 100% Non-Repetitive
# -----------------------------------------------------------
def generate_unique_content():
    topics = [
        "wealth creation", "ai automation", "global business", "mindset",
        "productivity", "ethical income", "mission 2040 growth",
        "digital freedom"
    ]

    topic = random.choice(topics)

    idea = (
        f"Fresh insight on {topic}: "
        f"Focus on {random.choice(['automation scale', 'deep value', 'trust building', 'system design', 'long-term consistency'])} "
        f"to accelerate legal passive growth."
    )

    unique_stamp = hashlib.sha256(str(random.random()).encode()).hexdigest()[:12]

    return f"{idea}\n#{topic.replace(' ', '')}_{unique_stamp}"


# -----------------------------------------------------------
# HUMAN MODE — Simulates safe natural behaviour
# -----------------------------------------------------------
def human_mode():
    actions = [
        "reading post", "liking content", "checking notifications",
        "scrolling slowly", "saving item", "light interaction"
    ]

    return {
        "mode": "human",
        "action": random.choice(actions),
        "delay": round(random.uniform(2.5, 8.0), 2)
    }


# -----------------------------------------------------------
# ROBO MODE — High-speed content engine
# -----------------------------------------------------------
def robo_mode():
    return {
        "mode": "robo",
        "action": "create_content",
        "content": generate_unique_content(),
        "count": random.randint(3, 6)   # more content due to aggressive mode
    }


# -----------------------------------------------------------
# BRAIN DECISION ENGINE — Aggressive Mode
# -----------------------------------------------------------
def brain_decision():
    if INTELLIGENCE_MODE == "conservative":
        ratio = 0.30  # 30% robo, 70% human
    elif INTELLIGENCE_MODE == "balanced":
        ratio = 0.60  # 60% robo, 40% human
    else:  # aggressive
        ratio = 0.85  # 85% robo, 15% human

    return robo_mode() if random.random() <= ratio else human_mode()


# -----------------------------------------------------------
# SAFE SERVICE REQUEST WRAPPER
# -----------------------------------------------------------
def safe_get(url):
    try:
        return requests.get(url, timeout=10).json()
    except Exception:
        return {"error": "service_down", "url": url}


def safe_post(url, payload):
    try:
        return requests.post(url, json=payload, timeout=10).json()
    except Exception:
        return {"error": "service_down", "url": url}


# -----------------------------------------------------------
# TASK QUEUE
# -----------------------------------------------------------
def queue_task(task):
    return safe_post(f"{BACKEND}/api/task/new", {"task": task, "lock": LOCK})


# -----------------------------------------------------------
# SERVICE TRIGGERS
# -----------------------------------------------------------
def run_intelligence():
    return safe_get(f"{BACKEND}/api/intelligence/run")


def run_memory():
    return safe_get(f"{MEMORY}/sync")


def run_reports():
    return safe_get(f"{REPORT}/generate")


# -----------------------------------------------------------
# MAIN LOOP — Runs Every Hour
# -----------------------------------------------------------
def main():
    while True:
        print("\n🔥 JRAVIS-BRAIN v4 — CYCLE START")

        # 1. Brain decision
        decision = brain_decision()
        print("🧠 Decision:", decision)

        # 2. Queue task
        q = queue_task(decision)
        print("📥 Task Queue:", q)

        # 3. Intelligence worker activation
        intel = run_intelligence()
        print("🤖 Intelligence:", intel)

        # 4. Memory sync for uniqueness
        mem = run_memory()
        print("💾 Memory:", mem)

        # 5. Daily & weekly reports
        rep = run_reports()
        print("📊 Reports:", rep)

        print("⏳ Sleeping 1 hour…\n")
        time.sleep(3600)


if __name__ == "__main__":
    main()
