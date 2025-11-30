# publishers/youtube_publisher.py

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER", "generated")


def publish_youtube_script(task):
    """
    Creates a full YouTube script for faceless channels.
    """
    print("🎬 Creating YouTube script...")

    try:
        prompt = """
        Write a full YouTube script (1300 words) for a viral short-video topic.
        Include:
        - Hook
        - Narration
        - Sections
        - Facts
        - Outro
        """

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )
        script = response.output_text

        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
        path = f"{OUTPUT_FOLDER}/youtube_script.txt"

        with open(path, "w", encoding="utf-8") as f:
            f.write(script)

        print("🎥 YouTube script generated.")
        return "YouTube script ready"

    except Exception as e:
        print("❌ YouTube Error:", e)
        return "YouTube script failed"
