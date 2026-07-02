from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from chat import generate_reply
from retriever import retriever

app = FastAPI(title="SHL Assessment Agent")


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest):

    # Build search query from the entire conversation
    search_text = " ".join(
        msg.content
        for msg in request.messages
        if msg.role == "user"
    )

    # Retrieve the most relevant SHL assessments
    results = retriever.search(search_text, top_k=20)

    # Generate the final JSON response
    response = generate_reply(request.messages, results)

    return response