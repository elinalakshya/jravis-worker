import logging
import time
import traceback
import sys
import os

# ==========================================================
# LOAD JRAVIS BRAIN
# ==========================================================
try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(BASE_DIR)
    from src.jravis_config import JRAVIS_BRAIN
    print("🧠 JRAVIS_BRAIN loaded successfully.")
except Exception as e:
    JRAVIS_BRAIN = {}
    print("⚠ WARNING: Failed to load JRAVIS_BRAIN — running SAFE MODE.")
    print("Error:", e)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("JRAVIS Worker")

# ==========================================================
# ENGINE IMPORT SAFETY WRAPPER
# ==========================================================
def try_import(module_path, func_name):
    try:
        module = __import__(module_path, fromlist=[func_name])
        return getattr(module, func_name)
    except Exception as e:
        logger.error(f"❌ Failed to load {func_name} from {module_path}: {e}")
        return None

# ==========================================================
# 7 ACTIVE STREAM ENGINES
# ==========================================================
ENGINE_MAP = {
    "Gumroad Template Engine":
        try_import("src.engines.gumroad_engine", "run_gumroad_engine"),

    "Payhip Template Engine":
        try_import("src.engines.payhip_engine", "run_payhip_engine"),

    "Template Machine Engine":
        try_import("src.engines.template_machine_engine", "run_template_machine_engine"),

    "Auto Blogging Engine":
        try_import("src.engines.auto_blogging_engine", "run_auto_blogging_engine"),

    "Newsletter Monetization Engine":
        try_import("src.engines.newsletter_content_engine", "run_newsletter_content_engine"),

    "Affiliate Funnel Engine":
        try_import("src.engines.affiliate_funnel_engine", "run_affiliate_funnel_engine"),

    "Shopify Digital Products Engine":
        try_import("src.engines.shopify_engine", "run_shopify_engine"),
}

# ==========================================================
# INACTIVE STREAMS (placeholders only)
# ==========================================================
INACTIVE_ENGINES = [
    "Printify POD",
    "Stationery Export",
    "Webflow Templates",
    "POD Mega Stores",
    "Multi-Market Uploaders",
    "Dropshipping Store",
    "Micro-SaaS"
]

# ==========================================================
# SAFE RUNNER
# ==========================================================
def safe_run(title, engine_func):
    if engine_func is None:
        logger.warning(f"⚠ {title} engine missing.")
        return

    try:
        logger.info(f"🟦 Running → {title}")
        engine_func()
        logger.info(f"✅ Completed → {title}")
    except Exception as e:
        logger.error(f"❌ ERROR in {title}: {e}")
        traceback.print_exc()

# ==========================================================
# ENFORCE BRAIN RULES
# ==========================================================
def enforce_brain():
    owner = JRAVIS_BRAIN.get("identity", {}).get("owner")
    logger.info(f"🧠 Checking identity… owner = {owner}")

    if owner != "Boss":
        logger.warning("⚠ Wrong owner — switching to SAFE MODE.")

# ==========================================================
# MAIN LOOP
# ==========================================================
def main():
    logger.info("💓 JRAVIS Worker Started...")
    enforce_brain()

    logger.info("🔥 Running Full Automation Cycle (7 Streams)...")

    # Run ACTIVE ENGINES only
    for name, engine in ENGINE_MAP.items():
        safe_run(name, engine)
        time.sleep(1)

    # Log inactive engines
    for name in INACTIVE_ENGINES:
        logger.info(f"⚪ {name} Engine is inactive — skipping.")

    logger.info("✨ Cycle complete. Sleeping for 10 minutes...")
    time.sleep(600)


if __name__ == "__main__":
    while True:
        main()
