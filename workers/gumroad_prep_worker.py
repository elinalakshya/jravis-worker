import os
import json
from datetime import datetime

def run_gumroad_prep():
    os.makedirs("data", exist_ok=True)

    log_file = "data/logs.json"

    product = {
        "platform": "gumroad",
        "title": "Daily Focus System",
        "price": 999,
        "timestamp": datetime.utcnow().isoformat(),
        "status": "DRAFT_PREPARED"
    }

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(product) + "\n")

    print("🟡 Gumroad draft prepared")
