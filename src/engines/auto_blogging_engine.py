# File: src/engines/auto_blogging_engine.py
from typing import Dict, Any
from src.openai_helper import openai_helper

def run_auto_blogging_engine() -> Dict[str, Any]:
    """
    Generates a long-form SEO blog article.
    """
    system_prompt = (
        "You are an SEO expert and content strategist. Produce a rank-worthy blog post."
    )

    user_prompt = (
        "Create a blog article with:\n"
        "- SEO Title\n"
        "- Meta Description\n"
        "- Introduction\n"
        "- 6 Detailed Sections with headers\n"
        "- Conclusion\n"
        "- 5 SEO keywords\n"
        "Tone: informative, expert, easy to read."
    )

    result = openai_helper.generate_text(system_prompt, user_prompt, tokens=1600)

    payload = {
        "type": "blog_article",
        "content": result
    }

    return openai_helper.format_payload("auto_blogging", payload)
