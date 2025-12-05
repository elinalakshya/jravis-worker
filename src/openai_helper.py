# File: openai_helper.py
# Location: /opt/render/project/src/openai_helper.py

import os
import time
from typing import List, Optional, Dict, Any
from openai import OpenAI, APIError, RateLimitError, APITimeoutError

class OpenAIHelper:
    """
    Centralized helper for all OpenAI calls.
    Advanced version:
    - Chat completions
    - Embeddings
    - Retry logic
    - Structured outputs for engines & publishers
    """

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("❌ OPENAI_API_KEY is not set")

        self.client = OpenAI(api_key=api_key)

    # ----------------------------------------------------------------------
    # CHAT COMPLETION (main generator for all engines)
    # ----------------------------------------------------------------------
    def generate_text(
        self,
        system_prompt: str,
        user_prompt: str,
        tokens: int = 1200,
        temperature: float = 0.8,
        retries: int = 3
    ) -> str:
        """
        Standard text generation for JRAVIS engines.
        """

        for attempt in range(retries):
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4.1",
                    max_tokens=tokens,
                    temperature=temperature,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ]
                )
                return response.choices[0].message.content.strip()

            except (RateLimitError, APITimeoutError):
                time.sleep(1.5 * (attempt + 1))
                continue

            except APIError as e:
                raise RuntimeError(f"OpenAI API failed: {str(e)}")

        raise RuntimeError("OpenAI request failed after multiple retries.")

    # ----------------------------------------------------------------------
    # EMBEDDINGS (for categorization, tagging, similarity)
    # ----------------------------------------------------------------------
    def get_embedding(self, text: str) -> List[float]:
        try:
            result = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            return result.data[0].embedding
        except Exception as e:
            raise RuntimeError(f"Embedding failed: {str(e)}")

    # ----------------------------------------------------------------------
    # JSON Output Helper for Engine Responses
    # ----------------------------------------------------------------------
    @staticmethod
    def format_payload(stream_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ensures that all engine-generated data has a consistent JSON structure.
        This is extremely important for n8n automation.
        """
        return {
            "stream": stream_name,
            "success": True,
            "data": data,
        }


# Singleton-style usage across JRAVIS
openai_helper = OpenAIHelper()
