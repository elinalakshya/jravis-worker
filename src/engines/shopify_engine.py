import logging
from openai import OpenAI

logger = logging.getLogger("ShopifyEngine")
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


def run_shopify_engine():
    """
    JRAVIS Shopify Digital Products Engine:
    Creates product listing copy for digital goods (no physical shipping).
    """
    logger.info("🟦 Running Shopify Digital Products Engine...")

    system_prompt = (
        "You are JRAVIS, a Shopify digital product copywriter. "
        "You write clean, persuasive product descriptions for instant-download products. "
        "No health, finance, or risky claims. Only safe, legal, evergreen products."
    )

    user_prompt = """
    Create a Shopify product listing for a digital product.

    Output as simple labeled sections:

    TITLE:
    SHORT_DESCRIPTION:
    LONG_DESCRIPTION:
    FEATURES:
    WHAT_YOU_GET:
    IDEAL_FOR:
    HOW_IT_WORKS:
    REFUND_POLICY:
    SEO_KEYWORDS:

    The product must be:
    - Instant download
    - No physical shipping
    - Clear about what the buyer receives
    - Easy to understand
    """

    try:
        listing = _ask_openai(user_prompt=user_prompt, system_prompt=system_prompt)
        logger.info("✅ Shopify digital product listing generated.")
        logger.debug(f"Shopify Listing:\n{listing}")

        # 🔹 HOOK POINT:
        # from publishers.shopify_publisher import create_shopify_product
        # create_shopify_product(listing)

    except Exception as e:
        logger.error(f"❌ Shopify Engine Error: {e}")
        raise
