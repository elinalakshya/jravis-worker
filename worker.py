import time
import requests
from settings import BACKEND_URL

# Import all publishers
from publishers.printify_publisher import publish_printify
from publishers.payhip_publisher import publish_payhip
from publishers.gumroad_publisher import publish_gumroad
from publishers.meshy_publisher import publish_meshy
from publishers.affiliate_blog_publisher import publish_affiliate_blog
from publishers.creative_market_publisher import publish_creative_market
from publishers.stock_media_publisher import publish_stock_media
from publishers.kdp_publisher import publish_kdp_book
from publishers.youtube_publisher import publish_youtube_video
from publishers.micro_niche_publisher import publish_micro_niche_site
from publishers.shopify_publisher import publish_shopify_item
from publishers.course_publisher import publish_course


def fetch_task():
    try:
        r = requests.get(f"{BACKEND_URL}/task/next")
        return r.json()
    except:
        return {"status": "error"}


def mark_done(task_id):
    try:
        requests.post(f"{BACKEND_URL}/task/done/{task_id}")
    except:
        pass


def process_task(task):
    t = task["task"]
    task_type = t["type"]

    print(f"📥 Received Task: {t}")

    # Routing table for task → function
    ROUTES = {
        "printify_pod": publish_printify,
        "payhip_upload": publish_payhip,
        "gumroad_upload": publish_gumroad,
        "meshy_assets": publish_meshy,
        "affiliate_blog": publish_affiliate_blog,
        "creative_market": publish_creative_market,
        "stock_media": publish_stock_media,
        "kdp_books": publish_kdp_book,
        "youtube_automation": publish_youtube_video,
        "micro_niche_sites": publish_micro_niche_site,
        "shopify_digital_products": publish_shopify_item,
        "course_automation": publish_course
    }

    if task_type not in ROUTES:
        print(f"⚠ Unknown task type: {task_type}")
        return

    try:
        ROUTES[task_type](t)
    except Exception as e:
        print("❌ Worker processing error:", str(e))


def run_worker():
    print("🚀 JRAVIS Worker Started — Publishing Mode ACTIVE")

    while True:
        task = fetch_task()

        if task.get("status") == "empty":
            time.sleep(2)
            continue

        try:
            process_task(task)
        except Exception as e:
            print("❌ Error:", str(e))

        mark_done(task["id"])
        print(f"✔ Marked task as done: {task['id']}")
        time.sleep(1)


if __name__ == "__main__":
    run_worker()
