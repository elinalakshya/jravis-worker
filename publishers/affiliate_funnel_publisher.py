# -----------------------------------------------------------
# AFFILIATE FUNNEL GENERATOR — JRAVIS Auto-Landing System
# -----------------------------------------------------------

import os

def create_affiliate_funnel(title: str, link: str):
    print(f"[FUNNEL] Creating affiliate funnel for {title}...")

    folder = "funnels"
    os.makedirs(folder, exist_ok=True)

    html_path = f"{folder}/{title.replace(' ', '_').lower()}.html"

    html = f"""
    <html>
    <head><title>{title}</title></head>
    <body>
        <h1>{title}</h1>
        <p>Grab it here: <a href="{link}">{link}</a></p>
    </body>
    </html>
    """

    with open(html_path, "w") as f:
        f.write(html)

    print(f"[FUNNEL] Saved at {html_path}")
    return {"status": "ok", "path": html_path}
