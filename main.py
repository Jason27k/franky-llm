import os
from fastapi import FastAPI
from openrouter import OpenRouter
import os

app = FastAPI()

from pydantic import BaseModel


class ChatRequest(BaseModel):
    prompt: str


class ChatResponse(BaseModel):
    response: str


def load_system_prompt():
    with open("system_prompt.md", "r") as f:
        return f.read()


system_prompt = load_system_prompt()


@app.get("/")
async def root():
    return {"message": "API is running"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    with OpenRouter(api_key=os.getenv("OPENROUTER_API_KEY")) as client:
        response_text = client.chat.send(
            model="deepseek-v4-pro",
            messages=[
                {
                    "content": system_prompt,
                    "role": "system",
                },
                {
                    "role": "user",
                    "content": request.prompt,
                },
            ],
        )
    return ChatResponse(response=response_text.choices[0].message.content)
