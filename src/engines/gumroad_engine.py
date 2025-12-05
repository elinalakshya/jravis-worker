import logging
from openai import OpenAI
from src.engines.openai_helper import ask_openai
from publishers.gumroad_publisher import save_gumroad_product

logger = logging.getLogger("GumroadEngine")

MULTIPLIER = 5   # 5X products per cycle

client = OpenAI()

SEO_KEYWORDS = [
    "AI template", "business planner", "startup toolkit", "productivity",
    "Notion template", "digital download", "finance tracker", "resume template",
    "printable planner", "marketing kit"
]


def build_prompt():
    return f"""
    Generate {MULTIPLIER} high-quality Gumroad digital products.

    For each product return:
    - SEO optimized title (using: {', '.join(SEO_KEYWORDS)})
    - 2-paragraph description
    - 10 SEO tags
    - File placeholder: TEMPLATE_FILE
    - Category: digital templates

    Format output as JSON list:
    [
      {{
        "title": "...",
        "description": "...",
        "tags": [...],
        "file": "TEMPLATE_FILE"
      }}
    ]
    """


def run_gumroad_engine():
    logger.info("🟦 Running Gumroad Template Engine...")

    try:
        response = ask_openai(
            system_prompt="You generate premium digital templates.",
            user_prompt=build_prompt()
        )

        import json
        products = json.loads(response)

        for p in products:
            save_gumroad_product(
                title=p["title"],
                description=p["description"],
                tags=p["tags"]
            )

        logger.info(f"✅ Gumroad product batch created: {len(products)} items")

    except Exception as e:
        logger.error(f"❌ Gumroad Engine Error: {e}")
