import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.routes.chat import router
from server.routes.document_routes import router as document_router


app = FastAPI(
    title="MediBot API",
    description="AI Medical Assistant using RAG",
    version="1.0.0"
)


app.include_router(router)
app.include_router(document_router)


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


@app.get("/")
def root():
    return {
        "message": "Welcome to MediBot API",
        "status": "running"
    }