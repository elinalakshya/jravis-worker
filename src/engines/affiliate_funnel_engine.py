import logging
from src.engines.openai_helper import ask_openai
from publishers.affiliate_funnel_publisher import save_funnel_page

logger = logging.getLogger("AffiliateFunnelEngine")


def parse_title(html):
    try:
        start = html.lower().find("<h1>")
        end = html.lower().find("</h1>")
        if start != -1 and end != -1:
            return html[start+4:end].strip()
    except:
        pass
    return "Affiliate Funnel Page"


def run_affiliate_funnel_engine():
    logger.info("🟦 Running Affiliate Funnel Engine...")

    try:
        system_prompt = (
            "You are JRAVIS, a high-ticket affiliate funnel builder. "
            "Generate clean HTML only — persuasive, unique, legal."
        )

        user_prompt = """
        Build a complete funnel page:
        - <h1>Title</h1>
        - Emotional hook
        - Problem statement
        - Product intro (use AFFILIATE_LINK)
        - 5 benefits
        - How it works (steps)
        - Testimonials (fictional but realistic)
        - CTA section using AFFILIATE_LINK
        Output only clean HTML.
        """

        html = ask_openai(system_prompt, user_prompt)

        if "JRAVIS_ERROR" in html:
            logger.error("❌ Funnel generation failed.")
            return

        html = html.replace("AFFILIATE_LINK", "https://your-affiliate-link.com")
        title = parse_title(html)

        # Save funnel as file
        file_data = {
            "filename": f"{title.replace(' ', '_')}.html",
            "content": html,
            "type": "html"
        }

        # Save for deployment (optional publisher)
        try:
            save_funnel_page(title, html)
        except:
            logger.warning("⚠ Unable to save funnel page locally.")

        output = {
            "engine": "affiliate_funnels",
            "status": "success",
            "title": title,
            "description": "High-quality affiliate funnel page.",
            "html": html,
            "text": None,
            "keywords": ["affiliate", "funnel", "landing page"],
            "files": [file_data],
            "metadata": {
                "category": "funnels",
                "platform": "universal",
                "affiliate_link": "https://your-affiliate-link.com"
            }
        }

        logger.info("✅ Affiliate Funnel Generated Successfully")
        return output

    except Exception as e:
        logger.error(f"❌ Affiliate Funnel Engine Error: {e}")
