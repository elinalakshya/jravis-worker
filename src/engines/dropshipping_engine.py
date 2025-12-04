import logging
logger = logging.getLogger("DropshippingEngine")


def run_dropshipping_engine():
    logger.info("⚪ Dropshipping Stream is inactive — skipping execution.")

    return {
        "engine": "dropshipping_store",
        "status": "inactive",
        "message": "This stream is disabled in JRAVIS Option1 mode."
    }
