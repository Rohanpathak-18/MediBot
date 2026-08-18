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

# Custom Styling - Modernized Dark Premium Theme
st.markdown(
    """
    <style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main Container Background */
    .stApp {
        background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
        color: #e6edf3;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #12161f !important;
        border-right: 1px solid #21262d;
    }

    .sidebar-brand {
        font-size: 26px;
        font-weight: 700;
        background: linear-gradient(90deg, #38bdf8 0%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
        margin-bottom: 8px;
    }

    .sidebar-description {
        color: #8b949e;
        font-size: 14px;
        line-height: 1.5;
        margin-bottom: 20px;
    }

    /* Hero Section Header */
    .main-title-container {
        text-align: center;
        padding: 20px 0 10px 0;
    }

    .main-title {
        font-size: 44px;
        font-weight: 800;
        background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
        margin-bottom: 8px;
    }

    .subtitle {
        text-align: center;
        color: #9ca3af;
        font-size: 16px;
        font-weight: 400;
        margin-bottom: 20px;
    }

    /* Modern Glassmorphic Medical Disclaimer */
    .disclaimer-card {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(8px);
        border-radius: 12px;
        padding: 12px 20px;
        text-align: center;
        color: #94a3b8;
        font-size: 13px;
        max-width: 800px;
        margin: 0 auto 30px auto;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }

    /* Chat Messages Styling */
    div[data-testid="stChatMessage"] {
        background: rgba(22, 27, 34, 0.6);
        border: 1px solid #21262d;
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(6px);
    }

    /* Expandable Source Documents Styling */
    div[data-testid="stExpander"] {
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
        background-color: #161b22 !important;
        overflow: hidden;
        margin-top: 10px;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #0d1117;
    }
    ::-webkit-scrollbar-thumb {
        background: #30363d;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #484f58;
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

    # Header section
    st.markdown(
        '''
        <div class="main-title-container">
            <div class="main-title">🩺 MediBot</div>
            <div class="subtitle">AI-powered medical information assistant</div>
        </div>
        ''',
        unsafe_allow_html=True
    )

    st.markdown(
        '''
        <div class="disclaimer-card">
            🛡️ <b>Notice:</b> MediBot provides informational responses based on its knowledge base. Always consult a qualified healthcare professional for medical advice.
        </div>
        ''',
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

                # Sources inside expandable section
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