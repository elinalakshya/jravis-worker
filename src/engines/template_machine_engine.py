# File: src/engines/template_machine_engine.py
from typing import Dict, Any
from src.openai_helper import openai_helper

def run_template_machine_engine() -> Dict[str, Any]:
    """
    Generates templates, frameworks, scripts, SOPs.
    """
    system_prompt = "You produce actionable templates, SOPs, and frameworks."

    user_prompt = (
        "Generate a reusable template pack with:\n"
        "- Framework title\n"
        "- Step-by-step instructions\n"
        "- Checklist\n"
        "- Use cases\n"
        "- Example outputs"
    )

    result = openai_helper.generate_text(system_prompt, user_prompt)

    payload = {
        "type": "template_pack",
        "content": result
    }

    return openai_helper.format_payload("template_machine", payload)
