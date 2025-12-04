import logging
from openai import OpenAI

logger = logging.getLogger("PayhipEngine")
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


def run_payhip_engine():
    """
    JRAVIS Phase-1: Create 1–2 Payhip-ready digital product specs
    (can reuse ideas from Gumroad but with different angle/name).
    """
    logger.info("🟦 Running Payhip Template Engine...")

    system_prompt = (
        "You are JRAVIS, an AI that creates digital products for Payhip. "
        "You must not copy from elsewhere. Everything must be original and helpful. "
        "Focus on simple, low-support, one-time purchase products (checklists, planners, sheets)."
    )

    user_prompt = """
    Create a single Payhip-ready digital product specification.

    Output JSON with keys:
    - title
    - subtitle
    - description
    - what_is_included: bullet list
    - ideal_for: bullet list
    - keywords: comma-separated SEO keywords
    - upsell_idea: one additional product we could sell later

    Make the tone friendly, clear, and benefit-driven.
    """

    try:
        content = _ask_openai(user_prompt=user_prompt, system_prompt=system_prompt)
        logger.info("✅ Payhip product spec generated.")
        logger.debug(f"Payhip Product JSON:\n{content}")

        # 🔹 HOOK POINT:
        # from publishers.payhip_publisher import publish_payhip_product
        # publish_payhip_product(content)

    except Exception as e:
        logger.error(f"❌ Payhip Engine Error: {e}")
        raise
