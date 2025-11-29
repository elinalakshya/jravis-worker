import requests
from settings import PRINTIFY_API_KEY, OPENAI_API_KEY

def publish_printify(task):
    print("🖨 Publishing Printify product...")

    # Generate product idea
    prompt = "Generate a unique POD design concept."
    design = "JRAVIS auto POD concept"

    print("🎨 Generated:", design)
    print("📦 Sent to Printify (simulated, API-key-ready).")
