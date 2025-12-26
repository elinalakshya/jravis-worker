from playwright.sync_api import sync_playwright
import json, datetime
from config.settings import ENABLE_PUBLISH

def run_printify():
    if ENABLE_PUBLISH:
        raise Exception("Publish not allowed")

    with open("data/pod_texts.json") as f:
        texts = json.load(f)

    text = texts[datetime.date.today().toordinal() % len(texts)]

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir="printify-session",
            headless=False
        )
        page = browser.new_page()
        page.goto("https://printify.com/app", timeout=60000)

        page.click("text=Create product")
        page.click("text=T-Shirt")
        page.click("text=Start designing")

        page.click("text=Text")
        page.fill("textarea", text)

        page.click("text=Save")

        print("✅ Printify draft created")
        browser.close()
