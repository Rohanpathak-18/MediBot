from fastapi import FastAPI

from fastapi.middleware.cors import (
    CORSMiddleware
)


# =========================================================
# APP
# =========================================================

app = FastAPI(

    title="MediBot API",

    description="AI Medical Assistant using RAG",

    version="1.0.0"

)


# =========================================================
# ROUTES
# =========================================================

from server.routes.chat import router as chat_router



app.include_router(
    chat_router
)

# =========================================================
# CORS
# =========================================================

origins = [

    "http://localhost:5173",

    "http://127.0.0.1:5173",

    "https://medibot-web.onrender.com"

]


app.add_middleware(

    CORSMiddleware,

    allow_origins=origins,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():

    return {

        "message": "Welcome to MediBot API",

        "status": "running"

    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/api/health")
def health():

    return {

        "status": "healthy",

        "service": "MediBot API"

    }
