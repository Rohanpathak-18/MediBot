import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Absolute imports for your routes and services
from server.routes.chat import router
from server.services.rag_service import ask_medibot
from server.routes.document_routes import router as document_router



app = FastAPI(
    title="MediBot API",
    description="AI Medical Assistant using RAG",
    version="1.0.0"
)

app.include_router(document_router)
app.include_router(router)


origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://medibot-web.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(router)



@app.get("/")
def root():
    return {
        "message": "Welcome to MediBot API",
        "status": "running"
    }



if __name__ == "__main__":
    import uvicorn
    # Render passes the PORT environment variable dynamically
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("server.main:app", host="0.0.0.0", port=port, reload=True)