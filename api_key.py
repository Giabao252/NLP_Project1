import os
import requests

GENAI_API_KEY = "sk-03c74eefb5354171872e1fa7ce20b0ae"

PURDUE_URL = "https://genai.rcac.purdue.edu/api/chat/completions"

def ask_ai(user_input):
    response = requests.post(
        PURDUE_URL,
        headers={
            "Authorization": f"Bearer {os.environ['GENAI_API_KEY']}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-oss:120b",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an assistant inside my application."
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()

    data = response.json()
    return data["choices"][0]["message"]["content"]


# Example
result = ask_ai("Explain recursion in simple terms.")
print(result)