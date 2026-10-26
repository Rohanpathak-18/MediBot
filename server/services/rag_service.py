import os
from pathlib import Path
from functools import lru_cache

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import RetrievalQA


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv()


# Project root
BASE_DIR = Path(__file__).resolve().parents[2]

# Load the server-local environment file regardless of the process cwd.
load_dotenv(BASE_DIR / "server" / ".env")


# Main FAISS vectorstore
DB_FAISS_PATH = BASE_DIR / "server" / "vectorstore" / "db_faiss"


GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# =========================================================
# EMBEDDINGS
# =========================================================

@lru_cache(maxsize=1)
def get_embedding_model():

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


# =========================================================
# LOAD FAISS VECTORSTORE
# =========================================================

@lru_cache(maxsize=1)
def get_vectorstore():

    embedding_model = get_embedding_model()

    print("Loading FAISS vectorstore...")
    print("FAISS path:", DB_FAISS_PATH)

    # Check folder
    if not DB_FAISS_PATH.exists():

        raise FileNotFoundError(
            f"FAISS vectorstore directory not found: "
            f"{DB_FAISS_PATH}"
        )

    # Check FAISS index
    index_file = DB_FAISS_PATH / "index.faiss"

    if not index_file.exists():

        raise FileNotFoundError(
            f"index.faiss not found at: {index_file}"
        )

    # Check pickle file
    pickle_file = DB_FAISS_PATH / "index.pkl"

    if not pickle_file.exists():

        raise FileNotFoundError(
            f"index.pkl not found at: {pickle_file}"
        )

    vectorstore = FAISS.load_local(
        str(DB_FAISS_PATH),
        embedding_model,
        allow_dangerous_deserialization=True
    )

    print("FAISS vectorstore loaded successfully.")

    return vectorstore


# =========================================================
# QA CHAIN
# =========================================================

@lru_cache(maxsize=1)
def get_qa_chain():

    vectorstore = get_vectorstore()


    # -----------------------------------------------------
    # Prompt
    # -----------------------------------------------------

    prompt_template = """
Use the pieces of information provided in the context to answer
the user's question.

Rules:

1. Use only information available in the provided context.
2. Do not make up medical information.
3. If the answer is not available in the context, say:
   "I don't know based on the provided medical information."
4. Keep the answer clear and concise.
5. Do not unnecessarily repeat the question.

Context:
{context}

Question:
{question}

Answer:
"""


    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=[
            "context",
            "question"
        ]
    )


    # -----------------------------------------------------
    # Groq API key
    # -----------------------------------------------------

    if not GROQ_API_KEY:

        raise ValueError(
            "GROQ_API_KEY is not configured."
        )


    # -----------------------------------------------------
    # LLM
    # -----------------------------------------------------

    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0.0,
        groq_api_key=GROQ_API_KEY,
        max_tokens=300
    )


    # -----------------------------------------------------
    # Retriever
    # -----------------------------------------------------

    retriever = vectorstore.as_retriever(
        search_kwargs={
            "k": 2
        }
    )


    # -----------------------------------------------------
    # Retrieval QA
    # -----------------------------------------------------

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={
            "prompt": prompt
        }
    )


    return qa_chain


# =========================================================
# ASK MEDIBOT
# =========================================================

def ask_medibot(user_query):

    if not user_query or not user_query.strip():

        raise ValueError(
            "Question cannot be empty."
        )


    qa_chain = get_qa_chain()


    response = qa_chain.invoke({
        "query": user_query.strip()
    })


    # IMPORTANT:
    # No comma after the closing }
    #
    # Previously:
    #
    # return {...},
    #
    # That returned a tuple instead of a dictionary.

    return {
        "result": response.get(
            "result",
            "I couldn't generate a response."
        ),

        "source_documents": response.get(
            "source_documents",
            []
        )
    }
