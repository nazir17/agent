import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.post("/example")
async def generate_text(req: PromptRequest):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GENAI_API_KEY"),
        temperature=0.7
    )

    response = llm.invoke(req.prompt)
    return {"response": response.content}