from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os



load_dotenv()


app = FastAPI()


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key_api_key=os.environ["GOOGLE_API_KEY"],
    streaming=True,
    temperature=0.7
)


prompt = ChatPromptTemplate.from_template("You are an AI agent. Answer the question:{input}")


async def generate_stream(prompt_text: str):
    chain = prompt | llm

    async for token in chain.astream({"input": prompt_text}):
        if token.content:
            yield token.content


@app.get("/stream")
async def stream_endpoint(request: Request, q: str):

    async def event_generator():
        async for token in generate_stream(q):
            if await request.is_disconnected():
                break
            yield f"data: {token}"
    return StreamingResponse(event_generator(), media_type="text/event-stream")