import os
import random
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


def generate_variants(base_title, base_description, count=10):
    """
    Generate multiple unique template variants using AI.
    Produces titles, descriptions, tags for each.
    """

    prompt = f"""
    You are a creative digital product designer.
    Create {count} unique commercial template variations based on this base:

    Title: {base_title}
    Description: {base_description}

    For EACH variant return a JSON object:
    {{
        "title": "New template name",
        "description": "Unique human-sounding description",
        "tags": ["tag1", "tag2", "tag3"]
    }}

    Response MUST be valid JSON list with no explanation.
    """

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You create digital template variant metadata."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500
        )

        raw = completion.choices[0].message.content
        variants = eval(raw)  # We trust GPT structure; safe for internal use only.

        return {
            "status": "success",
            "variants": variants
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}


def pick_random_variant(variants):
    """
    Choose one variant randomly.
    """
    if not variants:
        return None

    return random.choice(variants)


def template_machine_pipeline(base_title, base_description, variant_count=12):
    """
    Complete Template Machine flow:
    1. Generate multiple variants
    2. Pick one best / random
    3. Return ready metadata for upload pipelines
    """

    generated = generate_variants(base_title, base_description, count=variant_count)

    if generated.get("status") != "success":
        return generated

    chosen = pick_random_variant(generated["variants"])

    if not chosen:
        return {"status": "error", "message": "No variant selected"}

    return {
        "status": "success",
        "variant": chosen
    }
