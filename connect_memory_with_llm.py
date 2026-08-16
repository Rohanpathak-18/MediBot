import os
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace,HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_classic.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()

#step1 : setup LLM (mistral with huggingface)


HF_TOKEN = os.getenv("HF_TOKEN")

huggingface_repo_id = "Qwen/Qwen2.5-7B-Instruct"


def load_llm(huggingface_repo_id):
    llm = HuggingFaceEndpoint(
        repo_id=huggingface_repo_id,
        temperature=0.5,
        max_new_tokens=512,
        huggingfacehub_api_token=HF_TOKEN,
    )

    return ChatHuggingFace(llm=llm)
  
  
#step2 : connect LLM with FAISS & create a chain

DB_FAISS_PATH = "vectorstore/db_faiss"
CUSTOM_PROMPT_TEMPLATE = """
Use the pieces of information provided in the context to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Don't provide anything out of the given context.

Context: {context}
Question: {question}

Start the answer directly. No small talk please.
"""
def set_custom_prompt(custom_prompt_template):
  prompt = PromptTemplate(template=custom_prompt_template, input_variables=["context", "question"])
  return prompt


embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

#load database
db = FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)

#create
QA_chain = RetrievalQA.from_chain_type(
  llm=load_llm(huggingface_repo_id),
  chain_type="stuff",
  return_source_documents=True,
  retriever=db.as_retriever(search_kwargs={'k':3}),
  chain_type_kwargs={'prompt':set_custom_prompt(CUSTOM_PROMPT_TEMPLATE)}
)

#NOW INVOKE WITH A SINGLE QUERY

user_query=input("Write Query Here: ")
response = QA_chain.invoke({'query':user_query})
print("RESULT: ", response["result"])
print("source documents: ", response["source_documents"])

