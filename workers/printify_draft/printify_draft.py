from playwright.sync_api import sync_playwright
import json
import datetime

# --- SAFETY FLAGS ---
PUBLISH_ALLOWED = False
MAX_DRAFTS_PER_DAY = 1

# --- LOAD DATA ---
with open("pod_texts.json") as f:
    POD_TEXTS = json.load(f)

today_index = datetime.date.today().toordinal() % len(POD_TEXTS)
TEXT_TO_USE = POD_TEXTS[today_index]

def run():
    with sync_playwright() as p:
        # Use existing logged-in browser profile
        browser = p.chromium.launch_persistent_context(
            user_data_dir="printify-profile",
            headless=False
        )
        page = browser.new_page()

        # 1. Open Printify
        page.goto("https://printify.com/app", timeout=60000)

        # 2. Click Create Product (selectors are examples)
        page.click("text=Create product")

        # 3. Select product (example: T-shirt)
        page.click("text=T-Shirt")

        # 4. Start designing
        page.click("text=Start designing")

        # 5. Add TEXT
        page.click("text=Text")
        page.fill("textarea", TEXT_TO_USE)

        # (Font, color, alignment steps go here)

        # 6. SAVE AS DRAFT
        page.click("text=Save")

        # 7. HARD STOP
        if page.locator("text=Publish").is_visible():
            print("Publish button visible — STOPPING (as expected).")

        print("Draft created successfully.")

        browser.close()

if __name__ == "__main__":
    run()
