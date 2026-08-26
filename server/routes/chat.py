from fastapi import APIRouter
from pydantic import BaseModel

from server.services.rag_service import ask_medibot


router = APIRouter(
    prefix="/api/chat",
    tags=["Chat"]
)


class ChatRequest(BaseModel):
    question: str


@router.post("/")
def chat(request: ChatRequest):

    response = ask_medibot(request.question)

    return {
        "answer": response["result"]
    }