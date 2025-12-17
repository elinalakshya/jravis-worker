# ===============================
# JRAVIS UNIFIED ENGINE
# STREAM → R2 → GUMROAD (LIVE)
# ===============================

import os
import uuid
import zipfile
import requests

from src.engines.gumroad_engine import publish_to_gumroad

# -------------------------------
# ENV CONFIG
# -------------------------------
R2_ACCOUNT_ID = os.getenv("R2_ACCOUNT_ID")
R2_ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID")
R2_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY")
R2_BUCKET = os.getenv("R2_BUCKET")
R2_ENDPOINT = os.getenv("R2_ENDPOINT")
R2_PUBLIC_BASE_URL = os.getenv("R2_PUBLIC_BASE_URL")

if not all([
    R2_ACCOUNT_ID,
    R2_ACCESS_KEY_ID,
    R2_SECRET_ACCESS_KEY,
    R2_BUCKET,
    R2_ENDPOINT,
    R2_PUBLIC_BASE_URL
]):
    raise RuntimeError("❌ Missing R2 environment variables")

# -------------------------------
# R2 UPLOAD (S3 COMPATIBLE)
# -------------------------------
def upload_to_r2(local_zip_path: str, object_name: str) -> str:
    """
    Upload ZIP to Cloudflare R2 and return public URL
    """
    import boto3

    s3 = boto3.client(
        "s3",
        endpoint_url=R2_ENDPOINT,
        aws_access_key_id=R2_ACCESS_KEY_ID,
        aws_secret_access_key=R2_SECRET_ACCESS_KEY,
        region_name="auto"
    )

    s3.upload_file(
        Filename=local_zip_path,
        Bucket=R2_BUCKET,
        Key=object_name,
        ExtraArgs={
            "ContentType": "application/zip"
        }
    )

    public_url = f"{R2_PUBLIC_BASE_URL}/{object_name}"
    return public_url

# -------------------------------
# ZIP VALIDATION
# -------------------------------
def validate_zip(zip_path: str):
    if not zipfile.is_zipfile(zip_path):
        raise RuntimeError("❌ Invalid ZIP file")

# -------------------------------
# MAIN ENTRY
# -------------------------------
def run_all_streams_micro_engine(zip_path: str, template_name: str, backend_url: str):
    print(f"🚀 unified_engine START for {template_name}")

    if not os.path.exists(zip_path):
        raise FileNotFoundError(f"ZIP not found: {zip_path}")

    validate_zip(zip_path)

    # Generate unique object name
    object_name = f"{template_name}.zip"

    print("☁️ Uploading ZIP to R2...")
    r2_url = upload_to_r2(zip_path, object_name)
    print(f"✅ R2 Upload OK → {r2_url}")

    # ---------------------------
    # PUBLISH TO GUMROAD
    # ---------------------------
    print("💰 Publishing to Gumroad...")
    result = publish_to_gumroad(
        title=f"{template_name} Digital Asset",
        file_url=r2_url,
        price_usd=9
    )

    print("📊 ENGINE COMPLETE:", result)
    return result
