
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from server.services.rag_service import ask_medibot


# =========================================================
# ROUTER
# =========================================================

router = APIRouter(
    prefix="/api/chat",
    tags=["Chat"]
)


# =========================================================
# REQUEST MODEL
# =========================================================

class ChatRequest(BaseModel):
    message: str
    document_id: str | None = None


# =========================================================
# CHAT ENDPOINT
# =========================================================

@router.post("/")
def chat(request: ChatRequest):

    try:

        # Check empty message
        if not request.message.strip():

            raise HTTPException(
                status_code=400,
                detail="Message cannot be empty."
            )


        print(
            "Received question:",
            request.message
        )

        print(
            "Document ID:",
            request.document_id
        )


        # Ask MediBot
        response = ask_medibot(
            request.message
        )


        print(
            "MediBot response generated"
        )


        # Get answer
        answer = response.get(
            "result",
            "I couldn't generate a response."
        )


        # Convert source documents
        sources = []

        for document in response.get(
            "source_documents",
            []
        ):

            sources.append({
                "content": document.page_content,
                "metadata": document.metadata
            })


        # Return JSON expected by React
        return {
            "answer": answer,
            "sources": sources
        }


    except HTTPException:
        raise


    except Exception as error:

        print(
            "MediBot chat error:",
            repr(error)
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

