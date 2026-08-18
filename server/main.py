import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Use absolute import instead of relative dot import
from routes.chat import router
from services.rag_service import ask_medibot

# Usage inside a route or function:
# rag_service.ask_medibot(question)
# --------------------------------------------------
# Create FastAPI Application
# --------------------------------------------------

app = FastAPI(
    title="MediBot API",
    description="AI Medical Assistant using RAG",
    version="1.0.0"
)

# --------------------------------------------------
# CORS Configuration
# --------------------------------------------------

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "*"  # Append production frontend URLs here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Register Routes
# --------------------------------------------------

app.include_router(router)

# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "Welcome to MediBot API",
        "status": "running"
    }

# Entrypoint for local execution
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)