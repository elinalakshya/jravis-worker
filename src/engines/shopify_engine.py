# File: src/engines/shopify_engine.py
from typing import Dict, Any
from src.openai_helper import openai_helper

def run_shopify_engine() -> Dict[str, Any]:
    """
    Produces a Shopify product listing with SEO and conversion optimization.
    """
    system_prompt = "You are a Shopify product listing optimization specialist."

    user_prompt = (
        "Create a full Shopify product listing:\n"
        "- Product title\n"
        "- Short description\n"
        "- Full description\n"
        "- 10 features\n"
        "- SEO keywords\n"
        "- Suggested tags\n"
        "- Marketing angle"
    )

    result = openai_helper.generate_text(system_prompt, user_prompt)

    payload = {
        "type": "shopify_product",
        "content": result
    }

    return openai_helper.format_payload("shopify", payload)
