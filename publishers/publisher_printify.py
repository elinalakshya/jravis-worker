import requests
from settings import PRINTIFY_API_KEY, OPENAI_API_KEY

def publish_printify_product():
    print("🖼 Creating Printify product...")

    # Step 1: Create design prompt
    prompt = "Generate a unique POD t-shirt design idea about motivation."

    # Step 2: Call OpenAI
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    body = {"model": "gpt-4.1-mini", "input": prompt}

    response = requests.post(
        "https://api.openai.com/v1/responses",
        json=body,
        headers=headers
    )

    idea = response.json()["output"][0]["content"][0]["text"]

    print("✨ Design Concept:", idea)

    # Step 3: Send to Printify (mocked for now)
    print("📤 Uploading to Printify...")

    # TODO: Real Printify publish endpoint goes here

    print("✅ Printify product published!")
