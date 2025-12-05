import os
import logging

logger = logging.getLogger("PayhipPublisher")

OUTPUT_DIR = "output/payhip/"

# Ensure directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_payhip_product(title, description, tags):
    """
    Saves Payhip product metadata locally.
    JRAVIS will publish using uploader automation later.
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

        logger.info(f"📄 Payhip product saved locally: {filepath}")

    except Exception as e:
        logger.error(f"❌ Failed to save Payhip product: {e}")
