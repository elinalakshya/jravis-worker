import logging
from src.engines.openai_helper import ask_openai
from publishers.newsletter_content_publisher import save_newsletter_issue

logger = logging.getLogger("NewsletterEngine")

def run_newsletter_content_engine():
    logger.info("🟦 Running Newsletter Content Engine...")

    system_prompt = """
    Create a monetizable newsletter issue.
    Sections:
    - Catchy headline
    - Intro story
    - Main topic deep-dive
    - 3 actionable tips
    - Call-to-action
    """

    user_prompt = "Generate a newsletter issue with a strong hook."

    try:
        content = ask_openai(system_prompt, user_prompt)

        save_newsletter_issue(content)

        logger.info("✅ Newsletter issue generated.")
    except Exception as e:
        logger.error(f"❌ Newsletter Engine Error: {e}")
