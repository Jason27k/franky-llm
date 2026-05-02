import os
from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

app = FastAPI()


class ChatRequest(BaseModel):
    prompt: str


class ChatResponse(BaseModel):
    response: str


def load_system_prompt():
    with open("system_prompt.md", "r") as f:
        return f.read()


system_prompt = load_system_prompt()

# Initialize the Gemini client.
# Because we ran load_dotenv(), it will automatically find GEMINI_API_KEY.
client = genai.Client()


@app.get("/")
async def root():
    return {"message": "API is running"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # Call the Gemini API
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=request.prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
        ),
    )

    return ChatResponse(response=response.text)
