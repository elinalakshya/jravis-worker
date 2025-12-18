import os
import boto3

def upload_to_r2(local_file_path: str, object_name: str) -> str:
    s3 = boto3.client(
        "s3",
        endpoint_url=f"https://{os.environ['R2_ACCOUNT_ID']}.r2.cloudflarestorage.com",
        aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],
        region_name="auto"
    )

    bucket = os.environ["R2_BUCKET"]
    s3.upload_file(local_file_path, bucket, object_name)

    public_url = f"{os.environ['R2_PUBLIC_BASE_URL']}/{object_name}"
    print("☁️ Uploaded to R2 →", object_name)

    return public_url
