import os

from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_classic.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

from server.services.document_service import load_document_vectorstore


load_dotenv()


# =========================================================
# EXISTING MEDIBOT VECTORSTORE
# =========================================================

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DB_FAISS_PATH = BASE_DIR / "vectorstore" / "db_faiss"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing from .env file"
    )


# =========================================================
# EMBEDDING MODEL
# =========================================================

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# =========================================================
# LOAD EXISTING MEDICAL KNOWLEDGE
# =========================================================

db = FAISS.load_local(
    str(DB_FAISS_PATH),
    embedding_model,
    allow_dangerous_deserialization=True
)


# =========================================================
# PROMPT
# =========================================================

CUSTOM_PROMPT_TEMPLATE = """
Use the pieces of information provided in the context
to answer the user's question.

If the answer is available in the context, answer the
question using that information.

If the answer is NOT available in the context, say:

"I don't know based on the provided medical information."

Do not make up information.

Context:
{context}

Question:
{question}

Answer directly.
"""


def set_custom_prompt():

    prompt = PromptTemplate(
        template=CUSTOM_PROMPT_TEMPLATE,
        input_variables=[
            "context",
            "question"
        ]
    )

    return prompt


# =========================================================
# LLM
# =========================================================

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.0,
    groq_api_key=GROQ_API_KEY
)


# =========================================================
# NORMAL MEDIBOT QA CHAIN
# =========================================================

qa_chain = RetrievalQA.from_chain_type(

    llm=llm,

    chain_type="stuff",

    retriever=db.as_retriever(
        search_kwargs={
            "k": 3
        }
    ),

    return_source_documents=True,

    chain_type_kwargs={
        "prompt": set_custom_prompt()
    }
)


# =========================================================
# USER DOCUMENT QA CHAIN
# =========================================================

def create_document_qa_chain(vectorstore):

    qa_chain = RetrievalQA.from_chain_type(

        llm=llm,

        chain_type="stuff",

        retriever=vectorstore.as_retriever(
            search_kwargs={
                "k": 3
            }
        ),

        return_source_documents=True,

        chain_type_kwargs={
            "prompt": set_custom_prompt()
        }
    )

    return qa_chain


# =========================================================
# ASK MEDIBOT
# =========================================================

def ask_medibot(
    question: str,
    document_id: str | None = None
):

    # =====================================================
    # MODE 1: USER UPLOADED DOCUMENT
    # =====================================================

    if document_id:

        print(
            f"Using uploaded document: {document_id}"
        )

        vectorstore = load_document_vectorstore(
            document_id
        )

        qa_chain = create_document_qa_chain(
            vectorstore
        )

    # =====================================================
    # MODE 2: DEFAULT MEDICAL KNOWLEDGE
    # =====================================================

    else:

        print(
            "Using default MediBot medical knowledge"
        )

        qa_chain = globals()["qa_chain"]

    # =====================================================
    # RUN RAG
    # =====================================================

    response = qa_chain.invoke(
        {
            "query": question
        }
    )

    result = response["result"]

    source_documents = response[
        "source_documents"
    ]

    # =====================================================
    # FORMAT SOURCES
    # =====================================================

    sources = []

    for document in source_documents:

        sources.append(
            {
                "content": document.page_content,

                "page": document.metadata.get(
                    "page",
                    "N/A"
                ),

                "source": document.metadata.get(
                    "source",
                    "Unknown"
                )
            }
        )

    return {
        "answer": result,
        "sources": sources
    }