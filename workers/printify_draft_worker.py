import asyncio
import json
import datetime
from playwright.async_api import async_playwright
from config.settings import ENABLE_PUBLISH

async def run_printify_async():
    if ENABLE_PUBLISH:
        raise Exception("Publish not allowed")

    with open("data/pod_texts.json") as f:
        texts = json.load(f)

    text = texts[datetime.date.today().toordinal() % len(texts)]

    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir="printify-session",
            headless=False
        )
        page = await browser.new_page()

        await page.goto("https://printify.com/app", timeout=60000)
        await page.click("text=Create product")
        await page.click("text=T-Shirt")
        await page.click("text=Start designing")

        await page.click("text=Text")
        await page.fill("textarea", text)

        await page.click("text=Save")

        print("✅ Printify draft created (ASYNC)")
        await browser.close()

def run_printify():
    asyncio.run(run_printify_async())
