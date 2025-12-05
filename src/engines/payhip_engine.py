# File: src/engines/payhip_engine.py
from typing import Dict, Any
from src.openai_helper import openai_helper

def run_payhip_engine() -> Dict[str, Any]:
    """
    Generates a Payhip product listing with descriptions and value points.
    """
    system_prompt = (
        "You create high-converting digital products for Payhip."
    )

    user_prompt = (
        "Create a Payhip product package including:\n"
        "- Title\n"
        "- Overview\n"
        "- Benefit List (8 points)\n"
        "- Who this is for\n"
        "- What's included\n"
        "- Short sales pitch"
    )

    result = openai_helper.generate_text(system_prompt, user_prompt)

    payload = {
        "title": "Payhip Product",
        "content": result
    }

    return openai_helper.format_payload("payhip", payload)
