# File: src/engines/affiliate_funnel_engine.py
from typing import Dict, Any
from src.openai_helper import openai_helper

def run_affiliate_funnel_engine() -> Dict[str, Any]:
    """
    Creates a complete affiliate marketing funnel content pack.
    """
    system_prompt = (
        "You are an expert in direct-response and affiliate marketing."
    )

    user_prompt = (
        "Create a funnel content pack including:\n"
        "- Landing page headline\n"
        "- Sub-headline\n"
        "- Persuasive body content\n"
        "- 3 email sequence drafts\n"
        "- Bonus section\n"
        "- CTA section\n"
        "Tone: high-conversion, emotional, persuasive."
    )

    result = openai_helper.generate_text(system_prompt, user_prompt, tokens=1500)

    payload = {
        "type": "affiliate_funnel",
        "content": result
    }

    return openai_helper.format_payload("affiliate_funnel", payload)
