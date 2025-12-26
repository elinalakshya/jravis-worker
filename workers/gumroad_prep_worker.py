import json, datetime

def run_gumroad_prep():
    product = {
        "title": "Daily Focus System",
        "price": 999,
        "description": "A simple system to execute daily.",
        "status": "DRAFT_ONLY"
    }

    with open("data/logs.json", "a") as f:
        f.write(json.dumps(product) + "\n")

    print("🟡 Gumroad draft prepared")
