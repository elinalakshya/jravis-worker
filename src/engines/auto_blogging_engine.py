import logging
from openai import OpenAI

logger = logging.getLogger("AutoBloggingEngine")
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


def run_auto_blogging_engine():
    """
    JRAVIS Auto-Blogging Engine:
    Generate 1 high-quality blog article draft for programmatic SEO.
    """
    logger.info("🟦 Running Auto Blogging Engine...")

    system_prompt = (
        "You are JRAVIS, an SEO-aware blogger. "
        "You write helpful, human-sounding articles. "
        "No AI detection triggers, no keyword stuffing, no plagiarism. "
        "Short paragraphs, headings, and clear structure."
    )

    user_prompt = """
    Write one complete blog article on a safe, evergreen topic 
    that can attract organic search traffic and potential buyers
    for digital products (templates, planners, systems).

    Requirements:
    - 1200–1800 words
    - Use H2 and H3 headings
    - Add bullet lists where helpful
    - Tone: friendly, expert, real
    - No clickbait
    - No fake data or medical/financial claims
    """

    try:
        article = _ask_openai(user_prompt=user_prompt, system_prompt=system_prompt)
        logger.info("✅ Auto-blog article generated.")
        logger.debug(f"Auto-Blog Article:\n{article}")

        # 🔹 HOOK POINT:
        # from publishers.blog_publisher import publish_article
        # publish_article(article)

    except Exception as e:
        logger.error(f"❌ Auto Blogging Engine Error: {e}")
        raise
