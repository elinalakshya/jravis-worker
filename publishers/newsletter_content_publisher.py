import os

OUTPUT_DIR = "output/newsletters"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_newsletter_issue(title: str, html: str, md: str):
    safe_title = title.replace(" ", "_").replace("/", "_")

    html_path = os.path.join(OUTPUT_DIR, f"{safe_title}.html")
    md_path = os.path.join(OUTPUT_DIR, f"{safe_title}.md")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)

    return html_path, md_path
