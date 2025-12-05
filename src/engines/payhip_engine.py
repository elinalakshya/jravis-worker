import logging
from openai import OpenAI
from src.engines.openai_helper import ask_openai
from publishers.payhip_publisher import save_payhip_product

logger = logging.getLogger("PayhipEngine")

MULTIPLIER = 5
client = OpenAI()

SEO_KEYWORDS = [
    "digital planner", "AI sheet", "Ebook", "minimalist template",
    "business finance", "notion", "marketing plan", "goal tracker"
]


def build_prompt():
    return f"""
    Generate {MULTIPLIER} Payhip digital products.

    Each product should include:
    - Short strong title
    - Detailed description (SEO keyword rich)
    - 8–12 SEO tags
    - File placeholder: TEMPLATE_FILE

    Output JSON list only.
    """


def run_payhip_engine():
    logger.info("🟦 Running Payhip Template Engine...")

    try:
        response = ask_openai(
            system_prompt="You create high-conversion Payhip products.",
            user_prompt=build_prompt()
        )

        import json
        products = json.loads(response)

        for p in products:
            save_payhip_product(
                title=p["title"],
                description=p["description"],
                tags=p["tags"]
            )

        logger.info(f"✅ Payhip batch generated: {len(products)} items")

    except Exception as e:
        logger.error(f"❌ Payhip Engine Error: {e}")
