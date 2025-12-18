import os
from engines.r2_engine import upload_to_r2
from engines.gumroad_engine import create_gumroad_product

def run_all_streams_micro_engine(zip_path: str, template_name: str, backend_url=None):
    print("🚀 unified_engine START for", template_name)

    object_name = f"{template_name}.zip"

    # 1️⃣ Upload ZIP to R2
    content_url = upload_to_r2(zip_path, object_name)
    print("🔗 CONTENT URL =", content_url)

    # 2️⃣ Create Gumroad product
    create_gumroad_product(
        title=template_name,
        content_url=content_url,
        price_usd=9
    )

    print("📊 ENGINE COMPLETE: gumroad=success")
