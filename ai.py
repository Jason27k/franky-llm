from openrouter import OpenRouter
import os

with OpenRouter(api_key=os.getenv("OPENROUTER_API_KEY")) as client:
    response = client.chat.send(
        model="deepseek-v4-pro",
        messages=[
            {
                "role": "user",
                "content": "Are you able to teach me japanese? if so give me a lesson",
            }
        ],
    )

    print(response)
