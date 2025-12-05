import logging
from openai import OpenAI
from publishers.gumroad_publisher import save_gumroad_product

client = OpenAI()
logger = logging.getLogger("GumroadEngine")


def run_gumroad_engine():
    """Generates a Gumroad digital product + saves it for upload."""
    logger.info("🟦 Running Gumroad Template Engine...")

    try:
        prompt = """
        Create a complete Gumroad digital product template.
        Structure:
        - Product Title
        - Short Description
        - Features (list)
        - Who it's for
        - What's included
        - Pricing suggestion
        - Clean HTML layout ready for upload
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )

        html = response.choices[0].message.content

        # extract product title from <h1>
        title_start = html.find("<h1>")
        title_end = html.find("</h1>")

        if title_start != -1 and title_end != -1:
            title = html[title_start + 4:title_end].strip()
        else:
            title = "Gumroad_Product"

        save_gumroad_product(title, html)

        logger.info("✅ Gumroad Template generated successfully.")

    except Exception as e:
        logger.error(f"❌ Gumroad Engine Error: {e}")
