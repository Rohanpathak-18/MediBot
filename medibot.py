import os
import streamlit as st

from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_classic.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

load_dotenv()


# Page configuration
st.set_page_config(
    page_title="MediBot",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Custom styling
st.markdown(
    """
<style>
    .stApp {
        background-color: #0e1117;
    }

    section[data-testid="stSidebar"] {
        background-color: #151923;
    }

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #9aa4b2;
        font-size: 16px;
        margin-bottom: 30px;
    }

    .disclaimer {
        text-align: center;
        color: #737d8c;
        font-size: 12px;
        margin-top: 20px;
        margin-bottom: 30px;
    }

    div[data-testid="stChatMessage"] {
        border-radius: 15px;
        margin-bottom: 12px;
    }

    .sidebar-brand {
        font-size: 28px;
        font-weight: 700;
        color: white;
    }

    .sidebar-description {
        color: #9aa4b2;
        line-height: 1.6;
        margin-bottom: 25px;
    }
</style>
""",
    unsafe_allow_html=True
)


# Load FAISS vector database
DB_FAISS_PATH = "vectorstore/db_faiss"


@st.cache_resource
def get_vectorstore():

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = FAISS.load_local(
        DB_FAISS_PATH,
        embedding_model,
        allow_dangerous_deserialization=True
    )

    return db


# RAG prompt
def set_custom_prompt():

    custom_prompt_template = """
Use the pieces of information provided in the context to answer the user's question.

If the answer is available in the context, answer the question using that information.

If the answer is NOT available in the context, say:
"I don't know based on the provided medical information."

Do not make up information.

Context:
{context}

Question:
{question}

Answer directly.
"""

    return PromptTemplate(
        template=custom_prompt_template,
        input_variables=["context", "question"]
    )


# Sidebar
def create_sidebar():

    with st.sidebar:

        st.markdown(
            '<div class="sidebar-brand">🩺 MediBot</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="sidebar-description">'
            'Your AI-powered medical information assistant.'
            '</div>',
            unsafe_allow_html=True
        )

        if st.button(
            "🗑️ Clear Conversation",
            use_container_width=True
        ):
            st.session_state.messages = []
            st.rerun()

        st.divider()

        st.subheader("💡 About MediBot")

        st.write(
            "MediBot uses Retrieval-Augmented Generation "
            "(RAG) to retrieve relevant information from "
            "its medical knowledge base."
        )

        st.divider()

        st.subheader("⚙️ Technology")

        st.write(
            "• Streamlit\n\n"
            "• LangChain\n\n"
            "• FAISS\n\n"
            "• HuggingFace Embeddings\n\n"
            "• Groq LLM"
        )

        st.divider()

        st.subheader("⚠️ Disclaimer")

        st.caption(
            "MediBot provides medical information for "
            "educational purposes only. Always consult "
            "a qualified healthcare professional."
        )


# Main application
def main():

    create_sidebar()

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Header
    st.markdown(
        '<div class="main-title">🩺 MediBot</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'AI-powered medical information assistant'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="disclaimer">'
        'MediBot provides informational responses based on its '
        'knowledge base. Always consult a qualified healthcare '
        'professional for medical advice.'
        '</div>',
        unsafe_allow_html=True
    )

    # Display previous messages
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    prompt = st.chat_input(
        "Ask MediBot a medical question..."
    )

    if prompt:

        # Show user message
        with st.chat_message("user"):
            st.markdown(prompt)

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        try:

            # Load vector database
            vectorstore = get_vectorstore()

            if vectorstore is None:
                st.error("Failed to load vector store.")
                return

            # Create RAG chain
            qa_chain = RetrievalQA.from_chain_type(

                llm=ChatGroq(
                    model="openai/gpt-oss-20b",
                    temperature=0.0,
                    groq_api_key=os.environ["GROQ_API_KEY"]
                ),

                chain_type="stuff",

                retriever=vectorstore.as_retriever(
                    search_kwargs={"k": 3}
                ),

                return_source_documents=True,

                chain_type_kwargs={
                    "prompt": set_custom_prompt()
                }
            )

            # Generate answer
            response = qa_chain.invoke(
                {
                    "query": prompt
                }
            )

            result = response["result"]
            source_documents = response["source_documents"]

            # Display assistant response
            with st.chat_message("assistant"):

                st.markdown(result)

                # Sources are hidden inside an expandable section
                with st.expander("📚 Source Documents"):

                    for i, document in enumerate(
                        source_documents,
                        start=1
                    ):

                        st.markdown(
                            f"**Source {i}**"
                        )

                        st.write(
                            document.page_content
                        )

                        if document.metadata:

                            page = document.metadata.get(
                                "page",
                                "N/A"
                            )

                            st.caption(
                                f"Page: {page}"
                            )

            # Save response in chat history
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": result
                }
            )

        except Exception as e:

            st.error(
                f"Error: {str(e)}"
            )


if __name__ == "__main__":
    main()