import os

from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_classic.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq


load_dotenv()


# --------------------------------------------------
# Configuration
# --------------------------------------------------

DB_FAISS_PATH = "vectorstore/db_faiss"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing from .env file"
    )


# --------------------------------------------------
# Load Embedding Model
# --------------------------------------------------

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# --------------------------------------------------
# Load FAISS Vector Database
# --------------------------------------------------

db = FAISS.load_local(
    DB_FAISS_PATH,
    embedding_model,
    allow_dangerous_deserialization=True
)


# --------------------------------------------------
# Custom RAG Prompt
# --------------------------------------------------

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


# --------------------------------------------------
# Create RAG Chain
# --------------------------------------------------

qa_chain = RetrievalQA.from_chain_type(

    llm=ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0.0,
        groq_api_key=GROQ_API_KEY
    ),

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


# --------------------------------------------------
# Ask MediBot
# --------------------------------------------------

def ask_medibot(question: str):

    response = qa_chain.invoke(
        {
            "query": question
        }
    )

    result = response["result"]

    source_documents = response[
        "source_documents"
    ]

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