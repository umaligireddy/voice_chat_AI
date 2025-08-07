import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
cilent = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_gpt_response(user_input: str) -> str:
    try:
        response= cilent.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"An error occured while getting the GPT response: {e}")
        return "Failed to get OpenAI response."
    