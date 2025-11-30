# payhip_engine.py
import logging
from publishers.payhip_publisher import upload_payhip_product

logger = logging.getLogger(__name__)

def generate_payhip_template():
    return {
        "title": "Resume Canva Template",
        "price": "3.99",
        "file_url": "https://yourcdn.com/canva/resume-pack.zip"
    }

def run_payhip_engine():
    logger.info("🟦 Running Payhip Engine...")
    t = generate_payhip_template()
    return upload_payhip_product(t)
