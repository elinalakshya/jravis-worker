# src/unified_engine.py

import os
import zipfile
from src.publishing_engine import run_publishers

def extract_zip(zip_path: str, output_dir: str):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(output_dir)

    return output_dir


def run_all_streams_micro_engine(zip_path: str, template_name: str, backend: str):
    print(f"🚀 unified_engine START for {template_name}")

    extracted_path = extract_zip(
        zip_path,
        f"factory_output/extracted/{template_name}"
    )

    title = f"{template_name} Digital Asset"
    description = f"Auto-generated product from JRAVIS: {template_name}"

    print("💰 Triggering publishing engine...")
    results = run_publishers(title, description, extracted_path)

    print("✅ Publishing completed:", results)
    return results
