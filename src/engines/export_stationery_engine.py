import logging
from publishers.shopify_publisher import publish_shopify_product

logger = logging.getLogger(__name__)

def run_stationery_engine():
    logger.info("🟦 Running Stationery Export Engine...")

    task = {
        "type": "stationery",
        "title": "Hardcover Premium Notebook",
        "description": "AI-generated export stationery listing",
        "specs": ["Hardcover", "90 GSM paper", "A5 size"],
        "price": 8.99
    }

    try:
        publish_shopify_product(task)
        logger.info("✅ Stationery export task sent.")
    except Exception as e:
        logger.error(f"❌ Stationery engine error: {e}")
