import logging
import base64
from src.engines.openai_helper import ask_openai

logger = logging.getLogger("GumroadEngine")


def run_gumroad_engine():
    logger.info("🟦 Running Gumroad Template Engine...")

    try:
        system_prompt = (
            "You are JRAVIS, an expert digital product creator for Gumroad. "
            "Produce unique, legal, high-quality templates. Output must be HTML or text only."
        )

        user_prompt = """
        Create a premium digital template suitable for Gumroad.
        Content structure:
        - Title
        - Description
        - Editable text areas
        - Preview sample section
        - Instructions
        Format output as clean HTML.
        """

        html_content = ask_openai(system_prompt, user_prompt)

        if "JRAVIS_ERROR" in html_content:
            logger.error("❌ Gumroad generation failed.")
            return

        # Save file content
        file_data = {
            "filename": "gumroad_template.html",
            "content": html_content,
            "type": "html"
        }

        output = {
            "engine": "gumroad_templates",
            "status": "success",
            "title": "Gumroad Template",
            "description": "Auto-generated digital template for Gumroad.",
            "html": html_content,
            "text": None,
            "keywords": ["gumroad", "template", "digital product", "jrvis"],
            "files": [file_data],
            "metadata": {
                "category": "templates",
                "platform": "gumroad",
                "price": "5 - 15 USD"
            }
        }

        logger.info("✅ Gumroad Template Created Successfully")
        return output

    except Exception as e:
        logger.error(f"❌ Gumroad Engine Error: {e}")
