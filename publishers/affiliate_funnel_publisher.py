# -----------------------------------------------------------
# JRAVIS — Affiliate Funnel Page Generator
# Mission 2040 — Traffic Booster (Phase 1)
# -----------------------------------------------------------

import os
import datetime

FUNNEL_DIR = "funnels"
os.makedirs(FUNNEL_DIR, exist_ok=True)


# -----------------------------------------------------------
# HTML Template
# -----------------------------------------------------------
def build_funnel_html(template_name, gumroad, payhip):
    return f"""
    <html>
    <head>
        <title>{template_name} — Premium Template</title>
        <meta name="description" content="A high-converting design template from JRAVIS Automation. Monetize instantly.">
        <style>
            body {{
                font-family: Arial;
                padding: 40px;
                max-width: 800px;
                margin: auto;
                line-height: 1.6;
            }}
            .btn {{
                display: inline-block;
                padding: 12px 22px;
                margin: 8px 0;
                background: #000;
                color: #fff;
                border-radius: 6px;
                text-decoration: none;
                font-weight: bold;
            }}
        </style>
    </head>

    <body>
        <h1>🔥 {template_name} — Premium Template</h1>
        <p>
            This is a professionally generated template from JRAVIS — fully optimized for 
            content creators, entrepreneurs, and business owners.
        </p>

        <h3>Download Now:</h3>

        <a class="btn" href="{gumroad}?ref=jravis">Buy on Gumroad</a><br>
        <a class="btn" href="{payhip}?ref=jravis">Buy on Payhip</a>

        <p>Instant download • Commercial use • High converting design</p>

        <footer>
            <p style="margin-top:40px; font-size:14px;">
                Generated automatically by JRAVIS — Mission 2040 Automation Engine.
            </p>
        </footer>
    </body>
    </html>
    """


# -----------------------------------------------------------
# Save Funnel to File
# -----------------------------------------------------------
def save_funnel(template_name, html):
    safe_name = template_name.lower().replace(" ", "-")
    filename = os.path.join(FUNNEL_DIR, f"{safe_name}.html")

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

    return filename


# -----------------------------------------------------------
# MAIN ENTRY — Called by Unified Engine
# -----------------------------------------------------------
def publish_affiliate_funnel(template_name, gumroad_url, payhip_url):
    print(f"[Funnel] 🌀 Generating funnel for {template_name}...")

    html = build_funnel_html(template_name, gumroad_url, payhip_url)
    filename = save_funnel(template_name, html)

    print(f"[Funnel] ✅ Saved → {filename}")

    return {
        "status": "success",
        "file": filename
    }
