import os
import logging

logger = logging.getLogger("GumroadPublisher")

OUTPUT_DIR = "output/gumroad_products"


def ensure_output_dir():
    """Creates the folder if it doesn't exist."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR, exist_ok=True)


def slugify(text):
    """Converts product title into a safe filename."""
    return (
        text.lower()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
        .replace("-", "_")
        .strip()
    )


def save_gumroad_product(title: str, html_content: str):
    """
    Saves generated Gumroad product HTML into /output/gumroad_products/.
    This is the function JRAVIS worker imports.
    """
    ensure_output_dir()

    filename = f"{slugify(title)}.html"
    path = os.path.join(OUTPUT_DIR, filename)

    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html_content)

        logger.info(f"📦 Gumroad product saved → {path}")
        return path

    except Exception as e:
        logger.error(f"❌ Failed to save Gumroad product: {e}")
        raise
