import os
import boto3

R2_ACCOUNT_ID = os.getenv("R2_ACCOUNT_ID")
R2_ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID")
R2_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY")
R2_BUCKET = os.getenv("R2_BUCKET")

if not all([
    R2_ACCOUNT_ID,
    R2_ACCESS_KEY_ID,
    R2_SECRET_ACCESS_KEY,
    R2_BUCKET
]):
    raise RuntimeError("❌ R2 credentials not fully set")


def upload_file_to_r2(local_path: str, object_key: str):
    """
    Upload file to Cloudflare R2 using S3-compatible API
    """

    endpoint_url = f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com"

    s3 = boto3.client(
        "s3",
        endpoint_url=endpoint_url,
        aws_access_key_id=R2_ACCESS_KEY_ID,
        aws_secret_access_key=R2_SECRET_ACCESS_KEY,
        region_name="auto"
    )

    s3.upload_file(
        local_path,
        R2_BUCKET,
        object_key,
        ExtraArgs={"ACL": "public-read"}
    )

    print(f"☁️ Uploaded to R2 → {object_key}")
