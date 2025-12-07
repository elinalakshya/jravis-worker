import os
import requests

NEWSLETTER_API = os.getenv("NEWSLETTER_API_KEY", "")

def send_newsletter(title, link):
    if not NEWSLETTER_API:
        return {"status": "error", "msg": "Missing Newsletter API key"}

    url = "https://api.bervo.com/v1/send"

    payload = {
        "subject": f"New Template: {title}",
        "content": f"🔥 New Drop!\n\n{title}\n\nBuy here: {link}",
    }

    headers = {"Authorization": f"Bearer {NEWSLETTER_API}"}

    try:
        r = requests.post(url, json=payload, headers=headers)
        return {"status": "success", "response": r.text}
    except Exception as e:
        return {"status": "error", "msg": str(e)}
