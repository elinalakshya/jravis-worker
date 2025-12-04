import logging
from openai import OpenAI

logger = logging.getLogger("AffiliateFunnelEngine")
client = OpenAI()


def _ask_openai(user_prompt: str, system_prompt: str | None = None) -> str:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_prompt})

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7,
    )
    return resp.choices[0].message.content


def run_affiliate_funnel_engine():
    """
    JRAVIS Affiliate Funnel Engine:
    Builds one simple funnel page in HTML with placeholder AFFILIATE_LINK.
    """
    logger.info("🟦 Running Affiliate Funnel Engine...")

    system_prompt = (
        "You are JRAVIS, a conversion-focused affiliate funnel designer. "
        "You write clean HTML landing pages (no CSS, no JS), just structure and copy. "
        "No fake claims, no medical/financial promises, fully compliant."
    )

    user_prompt = """
    Create a single-page affiliate funnel in HTML.

    Structure:
    - <h1> Main headline
    - Subheadline (strong emotional hook)
    - Problem section
    - Solution section (introduce product with placeholder AFFILIATE_LINK)
    - 5 bullet-point benefits
    - Social proof (3 short testimonials, names can be generic)
    - FAQ section (3–5 Q&A)
    - Final CTA button using AFFILIATE_LINK

    Use only basic HTML tags: h1, h2, p, ul, li, a, div, span, etc.
    Do NOT include <html>, <head>, <body> tags, only the inner content.
    """

    try:
        html = _ask_openai(user_prompt=user_prompt, system_prompt=system_prompt)
        logger.info("✅ Affiliate funnel HTML generated.")
        logger.debug(f"Affiliate Funnel HTML:\n{html}")

        # 🔹 HOOK POINT:
        # from publishers.affiliate_funnel_publisher import save_funnel_page
        # save_funnel_page("Affiliate Funnel", html)

    except Exception as e:
        logger.error(f"❌ Affiliate Funnel Engine Error: {e}")
        raise
