import os
from src.publishing_engine import run_publishers

def run_all_streams_micro_engine(zip_path: str, title: str, backend: str):
    """
    Central execution point for monetization.
    This MUST ALWAYS publish if API keys exist.
    """

    print("🚀 unified_engine: START")
    print(f"📦 ZIP     : {zip_path}")
    print(f"📝 TITLE   : {title}")
    print(f"🌐 BACKEND : {backend}")

    description = f"Auto-generated digital product: {title}"

    try:
        results = run_publishers(
            title=title,
            description=description,
            zip_path=zip_path
        )

        print("✅ Publishing completed")
        print(results)
        return results

    except Exception as e:
        print("❌ Publishing failed:", e)
        return {"status": "failed", "error": str(e)}
