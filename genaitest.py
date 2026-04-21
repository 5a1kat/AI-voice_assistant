from google import genai
import os
import time
from config import apikey

client = genai.Client(api_key=apikey)


def ask_gemini(prompt):
    max_retries = 3

    # Configuration settings for the model
    config: dict[str, float | int] = {
        "temperature": 0.7,
        "max_output_tokens": 500,  # This is the correct parameter name for this SDK
        "top_p": 1,
    }

    for attempt in range(max_retries):
        try:
            # Generate content using the dynamic 'prompt' passed to the function
            response = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=prompt,
                config=config
            )
            return response.text

        except Exception as e:
            if "429" in str(e):
                print(f"Rate limit hit. Waiting 10 seconds... (Attempt {attempt + 1})")
                time.sleep(10)
            else:
                print(f"DEBUG ERROR: {e}")
                break  # Exit loop for non-rate-limit errors

    return "I'm having trouble connecting to my brain right now."