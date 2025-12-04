import logging
from openai import OpenAI

logger = logging.getLogger("NewsletterContentEngine")
client = OpenAI()


def _ask_openai(user_prompt: str, system_prompt: str | None = None) -> str:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_prompt})

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.65,
    )
    return resp.choices[0].message.content


def run_newsletter_content_engine():
    """
    JRAVIS Newsletter Monetization Engine:
    Generates 1 email issue designed to build trust + softly sell.
    """
    logger.info("🟦 Running Newsletter Content Engine...")

    system_prompt = (
        "You are JRAVIS, a newsletter copywriter. "
        "Your job is to build trust, provide value, and gently promote digital products. "
        "You must respect all legal and ethical standards."
    )

    user_prompt = """
    Create one newsletter email in this structure:

    SUBJECT:
    PREVIEW_TEXT:

    [Email Body]
    - Hook
    - Short story or insight
    - 3–5 practical tips
    - Soft promotion of a digital product (use a placeholder link: https://example.com/product)
    - Closing line and simple CTA

    Tone:
    - Helpful
    - Friendly
    - No hype
    """

    try:
        email_body = _ask_openai(user_prompt=user_prompt, system_prompt=system_prompt)
        logger.info("✅ Newsletter issue generated.")
        logger.debug(f"Newsletter Content:\n{email_body}")

        # 🔹 HOOK POINT:
        # from publishers.newsletter_publisher import queue_email
        # queue_email(email_body)

    except Exception as e:
        logger.error(f"❌ Newsletter Content Engine Error: {e}")
        raise
