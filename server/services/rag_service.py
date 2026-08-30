import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import RetrievalQA

load_dotenv()

DB_FAISS_PATH = "vectorstore/db_faiss"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# --------------------------------------------------
# 1. Load embeddings ONCE
# --------------------------------------------------

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# --------------------------------------------------
# 2. Load FAISS ONCE
# --------------------------------------------------

vectorstore = FAISS.load_local(
    DB_FAISS_PATH,
    embedding_model,
    allow_dangerous_deserialization=True
)


# --------------------------------------------------
# 3. Create retriever ONCE
# --------------------------------------------------

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 2}
)


# --------------------------------------------------
# 4. Prompt
# --------------------------------------------------

prompt_template = """
Use the provided medical context to answer the user's question.

Rules:
- Use only information from the context.
- Do not make up information.
- If the answer is not available in the context, say:
"I don't know based on the provided medical information."
- Answer clearly and concisely.

Context:
{context}

Question:
{question}

Answer:
"""

prompt = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)


# --------------------------------------------------
# 5. Create LLM ONCE
# --------------------------------------------------

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.0,
    groq_api_key=GROQ_API_KEY,
)


# --------------------------------------------------
# 6. Create QA chain ONCE
# --------------------------------------------------

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={
        "prompt": prompt
    }
)


# --------------------------------------------------
# 7. Ask MediBot
# --------------------------------------------------

def ask_medibot(user_query):

    response = qa_chain.invoke({
        "query": user_query
    })

    return {
        "result": response["result"],
        "source_documents": response["source_documents"]
    }