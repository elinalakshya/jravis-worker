# File: src/engines/gumroad_engine.py
from typing import Dict, Any
from src.openai_helper import openai_helper

def run_gumroad_engine() -> Dict[str, Any]:
    """
    Generates a high-quality digital product optimized for Gumroad.
    """
    system_prompt = (
        "You are a specialized product creator for Gumroad. "
        "Your goal is to generate a premium digital product that can sell independently."
    )

    user_prompt = (
        "Generate a full digital product package with:\n"
        "- Title\n"
        "- Strong Hook\n"
        "- Product Description\n"
        "- 10 Key Features\n"
        "- Target Audience\n"
        "- 3 Bonus Materials\n"
        "- Short Promo Pitch\n"
        "Make it high-value, unique, and market-ready."
    )

    result = openai_helper.generate_text(system_prompt, user_prompt)

    payload = {
        "title": "Gumroad Product",
        "content": result,
    }

    return openai_helper.format_payload("gumroad", payload)
