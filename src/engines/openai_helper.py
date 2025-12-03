from openai import OpenAI

client = OpenAI()

def ask_openai(system_prompt, user_prompt):
    """
    Unified helper for all JRAVIS engines.
    Prevents 'ChatCompletionMessage' errors.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
        )
        
        # NEW FORMAT
        return response.choices[0].message.content

    except Exception as e:
        return f"JRAVIS_ENGINE_ERROR: {str(e)}"
