import logging
from src.engines.openai_helper import ask_openai

logger = logging.getLogger("PayhipEngine")


def run_payhip_engine():
    logger.info("🟦 Running Payhip Template Engine...")

    try:
        system_prompt = (
            "You are JRAVIS, expert template creator for Payhip. "
            "Produce unique, legal, editable digital templates."
        )

        user_prompt = """
        Create a Payhip-ready digital template.
        Structure:
        - Title
        - Editable section
        - Usage instructions
        - Preview sample
        Output ONLY clean HTML.
        """

        html = ask_openai(system_prompt, user_prompt)

        if "JRAVIS_ERROR" in html:
            logger.error("❌ Payhip generation failed.")
            return

        file_data = {
            "filename": "payhip_template.html",
            "content": html,
            "type": "html"
        }

        output = {
            "engine": "payhip_templates",
            "status": "success",
            "title": "Payhip Template",
            "description": "Auto-generated Payhip digital template.",
            "html": html,
            "text": None,
            "keywords": ["payhip", "template", "digital"],
            "files": [file_data],
            "metadata": {
                "category": "templates",
                "platform": "payhip",
                "price": "5 - 15 USD"
            }
        }

        logger.info("✅ Payhip Template Created Successfully")
        return output

    except Exception as e:
        logger.error(f"❌ Payhip Engine Error: {e}")
