import logging
from openai import OpenAI

logger = logging.getLogger("TemplateMachineEngine")
client = OpenAI()


def _ask_openai(user_prompt: str, system_prompt: str | None = None) -> str:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_prompt})

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.6,
    )
    return resp.choices[0].message.content


def run_template_machine_engine():
    """
    JRAVIS Template Machine:
    Generate a small batch of template blueprints that can be
    turned into products across multiple marketplaces later.
    """
    logger.info("🟦 Running Template Machine Engine...")

    system_prompt = (
        "You are JRAVIS, a template system architect. "
        "You generate structured 'blueprints' for digital templates that can be "
        "implemented in Notion, Excel, Google Sheets, Canva, or PDF planners. "
        "Everything must be legal, ethical, and original."
    )

    user_prompt = """
    Create 3 template blueprints.

    Output as clear text sections like:

    TEMPLATE 1:
    Name:
    Purpose:
    Ideal User:
    Sections:
    Automations:
    Monetization Potential:

    TEMPLATE 2:
    ...

    TEMPLATE 3:
    ...

    Focus on areas like:
    - freelancers
    - students
    - small business owners
    - digital creators
    """

    try:
        blueprints = _ask_openai(user_prompt=user_prompt, system_prompt=system_prompt)
        logger.info("✅ Template Machine blueprints generated.")
        logger.debug(f"Template Machine Output:\n{blueprints}")

        # 🔹 HOOK POINT:
        # Save to file or database for later productization.

    except Exception as e:
        logger.error(f"❌ Template Machine Engine Error: {e}")
        raise
