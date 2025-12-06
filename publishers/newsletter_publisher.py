# -----------------------------------------------------------
# JRAVIS — Newsletter Auto Publisher (Bervo Integration)
# Mission 2040 — Free Traffic Engine
# -----------------------------------------------------------

import os
import requests
import datetime

BERVO_API_KEY = os.getenv("BERVO_API_KEY")
BERVO_LIST_ID = os.getenv("BERVO_LIST_ID")   # audience id


# -----------------------------------------------------------
# Build Newsletter HTML Body
# -----------------------------------------------------------
def build_email_html(template_name, links):
    html = f"""
    <html>
    <body style="font-family: Arial; line-height: 1.6; padding: 20px;">
        <h2>🔥 New JRAVIS Template Drop: {template_name}</h2>

        <p>Hi there! Here's a brand-new premium design template generated automatically by JRAVIS.</p>

        <p>Download links:</p>
        <ul>
            <li><a href="{links.get('gumroad', '#')}">Gumroad</a></li>
            <li><a href="{links.get('payhip', '#')}">Payhip</a></li>
        </ul>

        <p>Perfect for digital products, online businesses, content creators and more.</p>

        <p>— JRAVIS Automation Engine</p>
    </body>
    </html>
    """
    return html


# -----------------------------------------------------------
# Send Email via Bervo API
# -----------------------------------------------------------
def send_bervo_email(subject, html):
    try:
        url = "https://api.bervo.com/email/send"

        payload = {
            "api_key": Bervo_API_KEY,
            "list_id": Bervo_LIST_ID,
            "subject": subject,
            "html": html
        }

        resp = requests.post(url, json=payload, timeout=20)
        return resp.json()
    except Exception as e:
        print("[Newsletter] ❌ Error sending email:", e)
        return None


# -----------------------------------------------------------
# MAIN ENTRY — Called by Unified Engine
# -----------------------------------------------------------
def publish_newsletter(template_name, gumroad_url, payhip_url):
    print(f"[Newsletter] 📧 Sending blast for {template_name}...")

    if not BERVO_API_KEY or not BERVO_LIST_ID:
        return {"status": "error", "message": "Missing BERVO API credentials"}

    links = {
        "gumroad": gumroad_url,
        "payhip": payhip_url
    }

    subject = f"🔥 New Template Drop — {template_name}"
    html = build_email_html(template_name, links)

    result = send_bervo_email(subject, html)

    if not result:
        return {"status": "error", "message": "Newsletter send failed"}

    print("[Newsletter] ✅ Blast Sent Successfully!")
    return {"status": "success", "details": result}
