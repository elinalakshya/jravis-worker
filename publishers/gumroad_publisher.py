# File: publishers/gumroad_publisher.py
import os
import json
import time
from typing import Dict, Any

OUTPUT_DIR = "/opt/render/project/src/output/gumroad"

def ensure_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR, exist_ok=True)

def publish_gumroad(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Gumroad publisher (simulated).
    Saves engine-generated product data into JSON file.
    """
    ensure_output_dir()

    timestamp = int(time.time())
    filename = f"{OUTPUT_DIR}/gumroad_{timestamp}.json"

    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=4)

        return {
            "publisher": "gumroad",
            "success": True,
            "message": "Gumroad publish simulated successfully",
            "file": filename,
            "data": payload
        }

    except Exception as e:
        return {
            "publisher": "gumroad",
            "success": False,
            "error": str(e)
        }
