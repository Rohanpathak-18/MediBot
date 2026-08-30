
import os
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

DB_FAISS_PATH = "vectorstore/db_faiss"

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

    return FAISS.load_local(
        DB_FAISS_PATH,
        embedding_model,
        allow_dangerous_deserialization=True
    )


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
    # Groq LLM
    # -----------------------------------------------------

    if not GROQ_API_KEY:

        raise ValueError(
            "GROQ_API_KEY is not configured."
        )

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