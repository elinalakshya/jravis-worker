import logging
from src.engines.openai_helper import ask_openai

logger = logging.getLogger("NewsletterEngine")


def run_newsletter_content_engine():
    logger.info("🟦 Running Newsletter Monetization Engine...")

    try:
        system_prompt = (
            "You are JRAVIS, a newsletter expert. "
            "Create engaging, monetization-friendly newsletters that follow ethical rules."
        )

        user_prompt = """
        Create a monetizable newsletter with:
        - Engaging title
        - Short intro
        - 3 valuable sections
        - A recommended product with placeholder AFFILIATE_LINK
        - CTA at the end
        Format output as clean HTML.
        """

        html = ask_openai(system_prompt, user_prompt)

        if "JRAVIS_ERROR" in html:
            logger.error("❌ Newsletter generation failed.")
            return

        # Replace placeholder link
        html = html.replace("AFFILIATE_LINK", "https://your-newsletter-link.com")

        file_data = {
            "filename": "newsletter.html",
            "content": html,
            "type": "html"
        }

        output = {
            "engine": "newsletter_monetization",
            "status": "success",
            "title": "Newsletter Content",
            "description": "JRAVIS-generated monetizable newsletter.",
            "html": html,
            "text": None,
            "keywords": ["newsletter", "email", "monetization"],
            "files": [file_data],
            "metadata": {
                "category": "newsletter",
                "platform": "email",
                "cta_link": "https://your-newsletter-link.com"
            }
        }

        logger.info("✅ Newsletter Generated Successfully")
        return output

    except Exception as e:
        logger.error(f"❌ Newsletter Engine Error: {e}")
