# ============================================
# JRAVIS UNIFIED ENGINE – STEP 5 (INCOME SAFE)
# ============================================

import time
import traceback

# ------------------------------------------------
# IMPORT PUBLISHER ENGINES
# ------------------------------------------------
# Each engine MUST expose a function like:
# run_<platform>_engine(zip_path, template_name)

from publishers.gumroad_engine import run_gumroad_engine
from publishers.payhip_engine import run_payhip_engine
from publishers.shopify_engine import run_shopify_engine
# add more engines here as needed


# ------------------------------------------------
# RETRY + BACKOFF WRAPPER
# ------------------------------------------------
def run_with_retry(
    fn,
    *,
    label="task",
    max_retries=3,
    base_delay=2
):
    """
    Executes fn() with retry + exponential backoff.
    Never raises exception to caller.
    """

    attempt = 0

    while attempt <= max_retries:
        try:
            result = fn()
            return {
                "status": "success",
                "attempts": attempt + 1,
                "result": result
            }

        except Exception as e:
            attempt += 1

            if attempt > max_retries:
                return {
                    "status": "failed",
                    "attempts": attempt,
                    "error": str(e),
                    "trace": traceback.format_exc()
                }

            delay = base_delay * (2 ** (attempt - 1))
            print(
                f"⚠️ [{label}] failed "
                f"(attempt {attempt}/{max_retries}) "
                f"→ retrying in {delay}s"
            )
            time.sleep(delay)


# ------------------------------------------------
# UNIFIED ORCHESTRATOR
# ------------------------------------------------
def run_all_streams_micro_engine(zip_path, template_name, backend_url=None):
    """
    Main orchestration engine.
    One failure NEVER blocks others.
    Returns structured result object.
    """

    print("\n🚀 unified_engine START")
    print(f"📦 Template : {template_name}")
    print(f"📁 ZIP      : {zip_path}")

    results = {}

    # -----------------------------
    # GUMROAD
    # -----------------------------
    results["gumroad"] = run_with_retry(
        lambda: run_gumroad_engine(zip_path, template_name),
        label="gumroad"
    )

    # -----------------------------
    # PAYHIP
    # -----------------------------
    results["payhip"] = run_with_retry(
        lambda: run_payhip_engine(zip_path, template_name),
        label="payhip"
    )

    # -----------------------------
    # SHOPIFY
    # -----------------------------
    results["shopify"] = run_with_retry(
        lambda: run_shopify_engine(zip_path, template_name),
        label="shopify"
    )

    # ------------------------------------------------
    # SUMMARY LOG
    # ------------------------------------------------
    print("\n📊 ENGINE SUMMARY")
    for platform, info in results.items():
        print(
            f"- {platform}: "
            f"{info['status']} "
            f"(attempts={info.get('attempts')})"
        )

    # ------------------------------------------------
    # FINAL RESULT (for STEP 5.3 / 5.4)
    # ------------------------------------------------
    return {
        "template": template_name,
        "results": results
    }
