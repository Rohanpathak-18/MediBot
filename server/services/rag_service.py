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


def get_vectorstore():
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return FAISS.load_local(
        DB_FAISS_PATH,
        embedding_model,
        allow_dangerous_deserialization=True
    )


def get_qa_chain():

    vectorstore = get_vectorstore()

    prompt_template = """
Use the pieces of information provided in the context to answer the user's question.

If the answer is available in the context, answer using that information.

If the answer is NOT available in the context, say:
"I don't know based on the provided medical information."

Do not make up information.

Context:
{context}

Question:
{question}

Answer directly.
"""

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0.0,
        groq_api_key=GROQ_API_KEY
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(
            search_kwargs={"k": 3}
        ),
        return_source_documents=True,
        chain_type_kwargs={
            "prompt": prompt
        }
    )

    return qa_chain


def ask_medibot(user_query):

    qa_chain = get_qa_chain()

    response = qa_chain.invoke({
        "query": user_query
    })

    return {
        "result": response["result"],
        "source_documents": response["source_documents"]
    }