import logging
from src.engines.openai_helper import ask_openai
from publishers.payhip_publisher import save_payhip_product

logger = logging.getLogger("PayhipEngine")

def run_payhip_engine():
    logger.info("🟦 Running Payhip Template Engine...")

    system_prompt = """
    You are JRAVIS — expert template creator for Payhip.
    Create a clean digital product template.
    Include:
    - Product title
    - Description
    - Included files
    - Usage instructions
    - Who it’s for
    """

    user_prompt = "Generate a digital template suitable for Payhip buyers."

    try:
        content = ask_openai(system_prompt, user_prompt)

        save_payhip_product(content)

        logger.info("✅ Payhip Template Created Successfully")
    except Exception as e:
        logger.error(f"❌ Payhip Engine Error: {e}")
