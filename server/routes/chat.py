from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from server.services.rag_service import ask_medibot

router = APIRouter(
    prefix="/api",
    tags=["Chat"]
)



class ChatRequest(BaseModel):
    message: str



@router.get("/health")
def health_check():
    return {
        "success": True,
        "message": "MediBot API is running"
    }



@router.post("/chat")
def chat(request: ChatRequest):
    try:
        question = request.message.strip()

        if not question:
            raise HTTPException(
                status_code=400,
                detail="Message cannot be empty"
            )

        result = ask_medibot(question)

        return {
            "success": True,
            "answer": result["answer"],
            "sources": result["sources"]
        }

    except HTTPException:
        raise

    except Exception as e:
        print("ERROR:", str(e))
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )