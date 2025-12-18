import os
from engines.gumroad_engine import update_gumroad_content_url

R2_PUBLIC_BASE_URL = os.getenv("R2_PUBLIC_BASE_URL")

if not R2_PUBLIC_BASE_URL:
    raise RuntimeError("❌ R2_PUBLIC_BASE_URL missing")


def run_all_streams_micro_engine(template_name: str, zip_path: str):
    """
    FINAL CONTENT_URL MODE
    - ZIP already uploaded to R2 by worker
    - We only update Gumroad content_url
    """

    print(f"🚀 unified_engine START for {template_name}")

    filename = os.path.basename(zip_path)
    content_url = f"{R2_PUBLIC_BASE_URL}/{filename}"

    print("☁️ Using R2 public asset")
    print(f"🔗 CONTENT URL = {content_url}")

    result = update_gumroad_content_url(content_url)

    print("📊 ENGINE COMPLETE:", result)

    return result
