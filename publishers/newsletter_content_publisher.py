# File: publishers/newsletter_content_publisher.py
import os
import json
import time
from typing import Dict, Any

OUTPUT_DIR = "/opt/render/project/src/output/newsletter"

def ensure_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR, exist_ok=True)

def publish_newsletter(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Newsletter content publisher (simulated).
    Produces JSON ready for email automation (Beehiiv, Mailchimp, etc.)
    """
    ensure_output_dir()

    timestamp = int(time.time())
    filename = f"{OUTPUT_DIR}/newsletter_{timestamp}.json"

    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=4)

        return {
            "publisher": "newsletter",
            "success": True,
            "message": "Newsletter publish simulated",
            "file": filename,
            "data": payload
        }

    except Exception as e:
        return {
            "publisher": "newsletter",
            "success": False,
            "error": str(e)
        }
