import os
import logging

logger = logging.getLogger("GumroadPublisher")

OUTPUT_DIR = "output/gumroad/"

# Ensure directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_gumroad_product(title, description, tags):
    """
    Saves Gumroad product metadata locally.
    Later JRAVIS uploader will publish via API/web UI automation.
    """
    try:
        safe_title = title.replace(" ", "_").replace("/", "_")
        filepath = os.path.join(OUTPUT_DIR, f"{safe_title}.txt")

        content = (
            f"TITLE:\n{title}\n\n"
            f"DESCRIPTION:\n{description}\n\n"
            f"TAGS:\n{', '.join(tags)}\n"
        )

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        logger.info(f"📄 Gumroad product saved locally: {filepath}")

    except Exception as e:
        logger.error(f"❌ Failed to save Gumroad product: {e}")
