from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.chat import router


# --------------------------------------------------
# Create FastAPI Application
# --------------------------------------------------

app = FastAPI(
    title="MediBot API",
    description="AI Medical Assistant using RAG",
    version="1.0.0"
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


# --------------------------------------------------
# Register Routes
# --------------------------------------------------

app.include_router(
    router
)


# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------

@app.get("/")
def root():

    return {
        "message": "Welcome to MediBot API",
        "status": "running"
    }