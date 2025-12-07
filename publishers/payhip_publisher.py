import time

def publish_to_payhip(zip_path, title):
    print(f"[PAYHIP] Uploading {title}...")

    # Placeholder upload simulation
    time.sleep(1)

    return {
        "status": "success",
        "platform": "payhip",
        "product_url": f"https://payhip.com/{title.replace(' ', '').lower()}",
    }
