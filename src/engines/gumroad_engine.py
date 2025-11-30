# gumroad_engine.py
import logging
from publishers.gumroad_publisher import upload_gumroad_product

logger = logging.getLogger(__name__)

def generate_template():
    return {
        "title": "Instagram Carousel Template",
        "price": 5,
        "file_url": "https://yourcdn.com/templates/insta-pack.zip",
        "description": "Editable Canva templates."
    }

def run_gumroad_engine():
    logger.info("🟦 Running Gumroad Engine...")
    template = generate_template()
    return upload_gumroad_product(template)
