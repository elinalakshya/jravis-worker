import logging
from src.engines.openai_helper import ask_openai
from publishers.gumroad_publisher import save_gumroad_product

logger = logging.getLogger("GumroadEngine")

def run_gumroad_engine():
    logger.info("🟦 Running Gumroad Template Engine...")

    system_prompt = """
    You are JRAVIS — expert digital product creator.
    Create a HIGH-DEMAND Gumroad template.
    Output sections:
    - Title
    - Description
    - Features list
    - What's included
    - Ideal audience
    - Licensing terms
    """

    user_prompt = "Generate a premium digital template for Gumroad. Keep it unique and legal."

    try:
        content = ask_openai(system_prompt, user_prompt)

        save_gumroad_product(content)

        logger.info("✅ Gumroad product spec generated.")
    except Exception as e:
        logger.error(f"❌ Gumroad Engine Error: {e}")
