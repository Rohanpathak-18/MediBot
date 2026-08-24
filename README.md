# 🩺 MediBot — RAG-Powered Medical Information Assistant

MediBot is an **AI-powered medical information assistant** built using **Retrieval-Augmented Generation (RAG)**. It allows users to ask medical and healthcare-related questions and receive answers grounded in information retrieved from a medical knowledge base.

The project combines **Python, LangChain, Hugging Face, FAISS, Sentence Transformers, and Streamlit** to create an interactive AI-powered question-answering system.

> ⚠️ **Medical Disclaimer:** MediBot is an educational/informational tool and is **not a replacement for a qualified doctor, diagnosis, or professional medical advice**. Users should consult a healthcare professional for medical decisions, emergencies, diagnosis, or treatment.

---

## 📌 Table of Contents

* [Features](#-features)
* [How MediBot Works](#-how-medibot-works)
* [Architecture](#-architecture)
* [Technology Stack](#-technology-stack)
* [Project Structure](#-project-structure)
* [Installation](#-installation)
* [Environment Variables](#-environment-variables)
* [Preparing the Knowledge Base](#-preparing-the-knowledge-base)
* [Creating the FAISS Vector Store](#-creating-the-faiss-vector-store)
* [Running MediBot](#-running-medibot)
* [Example Questions](#-example-questions)
* [RAG Pipeline](#-rag-pipeline)
* [Why RAG](#-why-rag)
* [Key Components](#-key-components)
* [Future Improvements](#-future-improvements)
* [Limitations](#-limitations)
* [Use Cases](#-use-cases)
* [Troubleshooting](#-troubleshooting)
* [Security](#-security)
* [Contributing](#-contributing)
* [License](#-license)
* [Author](#-author)

---

# 🚀 Features

### 🤖 AI-Powered Medical Q&A

Users can ask natural-language questions and receive AI-generated responses based on the information retrieved from the configured medical knowledge base.

### 📚 Retrieval-Augmented Generation

Instead of relying only on the language model's internal knowledge, MediBot retrieves relevant information from documents before generating an answer.

### 🔎 Semantic Search

MediBot uses vector embeddings to find documents that are semantically related to the user's question.

### 🧠 Hugging Face LLM

The application integrates Hugging Face models through LangChain to generate natural-language responses.

### 🗂️ FAISS Vector Database

FAISS is used to store and efficiently search document embeddings.

### 📄 Document-Based Knowledge

Medical information can be prepared from trusted documents and converted into a searchable knowledge base.

### 🎨 Streamlit Interface

The application provides an interactive web interface where users can enter questions and view generated responses.

### 🌙 Modern UI

MediBot includes a customized interface with a clean, modern dark-themed design and responsive components.

### 🔐 Environment-Based Configuration

Sensitive credentials such as Hugging Face API tokens are loaded using environment variables instead of being hard-coded.

---

# 🧠 How MediBot Works

MediBot follows the following workflow:

```text
                    USER
                     │
                     ▼
             Enter Medical Question
                     │
                     ▼
              Query Processing
                     │
                     ▼
          Convert Question to Embedding
                     │
                     ▼
             FAISS Vector Search
                     │
                     ▼
          Retrieve Relevant Documents
                     │
                     ▼
       ┌─────────────────────────────┐
       │       Retrieved Context     │
       └─────────────────────────────┘
                     │
                     ▼
             Prompt Construction
                     │
                     ▼
             Hugging Face LLM
                     │
                     ▼
            Generated Response
                     │
                     ▼
                  USER
```

The important idea is that the LLM receives **relevant retrieved context along with the user's question** before generating its answer.

---

# 🏗️ Architecture

MediBot follows a standard Retrieval-Augmented Generation architecture.

```text
                 ┌──────────────────┐
                 │   Medical PDFs   │
                 │   / Documents    │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Document Loader  │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Text Splitter    │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Embedding Model  │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ FAISS Vector DB  │
                 └────────┬─────────┘
                          │
                          │ Retrieval
                          ▼
User Question ──► Retriever
                     │
                     ▼
              Relevant Context
                     │
                     ▼
              Prompt Template
                     │
                     ▼
              Hugging Face LLM
                     │
                     ▼
               Final Answer
```

---

# 🛠️ Technology Stack

| Category                | Technology            |
| ----------------------- | --------------------- |
| Programming Language    | Python                |
| UI Framework            | Streamlit             |
| AI Framework            | LangChain             |
| LLM Provider            | Hugging Face          |
| Vector Database         | FAISS                 |
| Embeddings              | Sentence Transformers |
| Environment Management  | python-dotenv         |
| Model Integration       | Hugging Face Hub      |
| Development Environment | VS Code               |
| Version Control         | Git & GitHub          |

---

# 📁 Project Structure

A typical MediBot project structure is:

```text
MediBot/
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
│
├── data/
│   └── medical_documents/
│       └── medical_information.pdf
│
├── vectorstore/
│   └── db_faiss/
│       ├── index.faiss
│       └── index.pkl
│
└── assets/
    └── images/
```

Depending on the version of the project, document ingestion and vector-store creation may be placed in separate Python files.

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/MediBot.git
```

Navigate into the project:

```bash
cd MediBot
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If you do not have a `requirements.txt`, install the main dependencies:

```bash
pip install streamlit
pip install langchain
pip install langchain-community
pip install langchain-core
pip install langchain-huggingface
pip install huggingface_hub
pip install sentence-transformers
pip install faiss-cpu
pip install python-dotenv
pip install transformers
pip install torch
```

---

# 🔑 Environment Variables

Create a `.env` file in the root directory:

```env
HF_TOKEN=your_huggingface_access_token
```

The token is used to authenticate requests to Hugging Face models.

### Important

Never commit your `.env` file to GitHub.

Add this to `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
```

---

# 📚 Preparing the Knowledge Base

The quality of a RAG application depends heavily on the quality of its knowledge base.

Medical documents can be collected from reliable sources and placed inside the project's document directory.

Example:

```text
data/
└── medical_documents/
    ├── medical_encyclopedia.pdf
    ├── healthcare_guide.pdf
    └── medical_reference.pdf
```

The documents are then processed into smaller text chunks.

---

# 🧩 Document Processing

The general document-processing pipeline is:

```text
Documents
    ↓
Load Documents
    ↓
Extract Text
    ↓
Split Text into Chunks
    ↓
Generate Embeddings
    ↓
Store Embeddings
    ↓
FAISS Vector Database
```

Chunking is important because sending an entire large document to an LLM is inefficient.

Instead, the document is divided into smaller sections that can be retrieved when needed.

---

# 🗃️ FAISS Vector Store

MediBot uses FAISS to perform similarity search.

The project uses an embedding model such as:

```text
sentence-transformers/all-MiniLM-L6-v2
```

The embedding model converts text into numerical vectors.

For example:

```text
"What are symptoms of fever?"
             ↓
       Embedding Model
             ↓
[0.12, -0.42, 0.83, ...]
```

The vector is compared against vectors stored in FAISS to find semantically similar content.

---

# 🧠 RAG Pipeline

The complete RAG pipeline can be divided into two stages.

## Stage 1 — Indexing

```text
Medical Documents
       ↓
Document Loader
       ↓
Text Splitting
       ↓
Embedding Model
       ↓
FAISS
```

This stage creates the searchable knowledge base.

---

## Stage 2 — Question Answering

```text
User Question
      ↓
Question Embedding
      ↓
FAISS Similarity Search
      ↓
Relevant Documents
      ↓
Prompt Template
      ↓
LLM
      ↓
Answer
```

---

# 📝 Prompt Engineering

MediBot uses a prompt template to control how the language model generates its response.

A simplified prompt can look like:

```text
You are MediBot, a medical information assistant.

Use the provided context to answer the user's question.

If the answer cannot be found in the provided context,
do not make up information.

Context:
{context}

Question:
{question}

Answer:
```

This helps reduce unsupported answers and encourages the model to rely on retrieved information.

---

# 🤗 Hugging Face Integration

MediBot uses Hugging Face models through LangChain.

The application can use components such as:

```python
from langchain_huggingface import HuggingFaceEndpoint
from langchain_huggingface import ChatHuggingFace
```

A Hugging Face endpoint can be configured using the API token stored in `.env`.

Example:

```python
llm = HuggingFaceEndpoint(
    repo_id="your-model",
    huggingfacehub_api_token=HF_TOKEN
)
```

The exact model can be changed depending on available Hugging Face models and hardware/API availability.

---

# 🔍 Retrieval

The FAISS retriever searches for documents that are most relevant to the user's question.

Conceptually:

```python
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)
```

Here, `k=3` means the retriever attempts to provide the three most relevant document chunks as context.

---

# 💬 Example Questions

Users can ask questions such as:

```text
What are the common symptoms of fever?
```

```text
What are the symptoms of dehydration?
```

```text
What causes headaches?
```

```text
What are common symptoms of the flu?
```

```text
What are the symptoms of vitamin deficiency?
```

The application retrieves relevant information from the knowledge base before generating the response.

---

# 🖥️ Running MediBot

After configuring the environment and vector database, run:

```bash
streamlit run app.py
```

Streamlit will start the local development server.

You can then open the displayed local URL in your browser.

---

# 📦 Requirements

A typical `requirements.txt` may contain:

```text
streamlit
langchain
langchain-community
langchain-core
langchain-huggingface
huggingface_hub
sentence-transformers
faiss-cpu
python-dotenv
transformers
torch
```

Package versions may need adjustment depending on your Python version and the LangChain/Hugging Face APIs used by the project.

---

# 🧱 Key Components

## 1. Streamlit

Responsible for the web interface.

```text
User
 ↓
Streamlit UI
 ↓
Backend RAG Pipeline
 ↓
Response
```

---

## 2. LangChain

LangChain connects the major components of the RAG system:

```text
Retriever
    +
Prompt
    +
LLM
    ↓
Answer
```

---

## 3. Hugging Face

Provides access to language models used to generate responses.

---

## 4. Sentence Transformers

Converts questions and document chunks into embeddings.

---

## 5. FAISS

Stores and searches vector representations efficiently.

---

## 6. dotenv

Loads environment variables securely from `.env`.

---

# 🔄 End-to-End Example

Suppose the user asks:

```text
What are the symptoms of dehydration?
```

### Step 1 — User Query

The question enters MediBot.

### Step 2 — Embedding

The question is converted into a vector.

### Step 3 — Similarity Search

FAISS searches the medical knowledge base.

### Step 4 — Retrieval

Relevant chunks discussing dehydration are retrieved.

### Step 5 — Prompt

The retrieved information is inserted into the prompt.

### Step 6 — LLM

The Hugging Face model processes the prompt.

### Step 7 — Response

MediBot generates a natural-language answer.

```text
User Question
      ↓
Embedding
      ↓
FAISS
      ↓
Relevant Medical Context
      ↓
Prompt
      ↓
Hugging Face LLM
      ↓
MediBot Response
```

---

# ⭐ Why RAG?

Traditional LLM applications can have problems such as:

* Hallucinations
* Outdated knowledge
* Lack of domain-specific information
* Difficulty controlling the information used to generate answers

RAG addresses these problems by retrieving relevant information from an external knowledge source.

Instead of:

```text
Question → LLM → Answer
```

MediBot uses:

```text
Question
   ↓
Retrieve Information
   ↓
Relevant Context
   ↓
LLM
   ↓
Answer
```

This makes the application more suitable for knowledge-base-driven question answering.

---

# 🔐 Security Considerations

MediBot should follow good security practices.

### Never expose API keys

Do not hard-code:

```python
HF_TOKEN = "actual-secret-token"
```

Use:

```env
HF_TOKEN=your_token
```

and load it through environment variables.

### Do not commit `.env`

Use:

```gitignore
.env
```

### Validate User Input

User input should be handled safely before processing.

### Protect Sensitive Documents

If private medical documents are added in future versions, appropriate access control and storage security should be implemented.

---

# ⚠️ Medical Safety

MediBot should be treated as an **educational information assistant**, not a doctor.

It should not be used as the sole basis for:

* Diagnosis
* Prescription decisions
* Emergency treatment
* Medication dosage decisions
* Serious medical decisions

A production version should include stronger safety mechanisms, such as:

* Medical safety prompts
* Emergency-response detection
* Doctor consultation recommendations
* Source attribution
* Confidence indicators
* Guardrails against unsafe medical advice
* Human/medical-professional review

---

# 📈 Future Improvements

Several improvements can make MediBot more powerful.

## 👤 User Authentication

Add:

```text
Signup
Login
JWT Authentication
User Profiles
```

---

## 📄 User Document Upload

Allow users to upload their own:

```text
PDF
DOCX
TXT
```

documents.

The system can then:

```text
Upload Document
       ↓
Extract Text
       ↓
Chunk Text
       ↓
Generate Embeddings
       ↓
Create/Update Vector Store
       ↓
Ask Questions
```

This would turn MediBot into a personalized document-based medical assistant.

---

## 💾 Persistent Vector Database

Instead of creating a temporary vector store, the project can use:

* FAISS
* ChromaDB
* Pinecone
* Weaviate
* Qdrant

depending on project requirements.

---

## 🧠 Conversation Memory

Add chat history so users can ask follow-up questions.

Example:

```text
User:
What are the symptoms of dehydration?

MediBot:
...

User:
How can I prevent it?

MediBot:
...
```

---

## 📚 Source Citations

The application can display the document sources used to generate each answer.

Example:

```text
Answer generated using:

📄 Medical Encyclopedia
📄 Healthcare Reference Guide
```

---

## 🎙️ Voice Interaction

Future versions could support:

```text
Speech → Text → RAG → Answer → Text-to-Speech
```

---

## 🌐 Multilingual Support

The system could support languages such as:

* English
* Hindi
* Hinglish

This would make the application more accessible to Indian users.

---

# 🧪 Testing

MediBot should be tested using questions with known answers from the knowledge base.

Example test categories:

### Retrieval Testing

```text
Does MediBot retrieve the correct document?
```

### Answer Testing

```text
Does the generated answer match the retrieved context?
```

### Hallucination Testing

```text
Does the model avoid inventing information?
```

### Edge Cases

```text
Empty question
Very long question
Irrelevant question
Medical emergency question
Unknown medical condition
```

---

# 🐛 Troubleshooting

## Hugging Face Authentication Error

If you receive an authentication error, verify:

```env
HF_TOKEN=your_valid_token
```

and make sure the model is accessible to your account.

---

## FAISS Not Found

Install:

```bash
pip install faiss-cpu
```

---

## Sentence Transformers Error

Install:

```bash
pip install sentence-transformers
```

---

## LangChain Import Errors

LangChain packages are split across multiple packages in newer versions.

Try installing:

```bash
pip install -U langchain langchain-community langchain-core langchain-huggingface
```

---

## Vector Store Not Found

Make sure the expected directory exists:

```text
vectorstore/
└── db_faiss/
```

If it does not exist, run the document ingestion/vector-store creation script first.

---

## Python Version Issues

Some AI/ML packages may have compatibility issues with newer Python releases.

If dependency installation fails, consider using a stable Python version such as Python 3.11 or another version supported by the packages in your environment.

---

# 📊 Project Workflow Summary

```text
                ┌───────────────┐
                │ Medical Data  │
                └───────┬───────┘
                        ↓
                ┌───────────────┐
                │ Text Chunks   │
                └───────┬───────┘
                        ↓
                ┌───────────────┐
                │  Embeddings   │
                └───────┬───────┘
                        ↓
                ┌───────────────┐
                │     FAISS     │
                └───────┬───────┘
                        ↓
User ────────► Question
                        ↓
                ┌───────────────┐
                │   Retriever   │
                └───────┬───────┘
                        ↓
                ┌───────────────┐
                │    Context    │
                └───────┬───────┘
                        ↓
                ┌───────────────┐
                │ Prompt + LLM  │
                └───────┬───────┘
                        ↓
                ┌───────────────┐
                │    Answer     │
                └───────────────┘
```

---

# 🎯 Use Cases

MediBot can be used for:

* Medical education
* Healthcare information retrieval
* Student projects
* RAG demonstrations
* AI/ML learning
* Natural-language document search
* Medical knowledge exploration
* Generative AI experimentation

---

# 🚀 Learning Outcomes

This project demonstrates practical experience with:

* Retrieval-Augmented Generation
* Large Language Models
* Prompt Engineering
* Vector Embeddings
* Semantic Search
* Vector Databases
* LangChain
* Hugging Face
* Python
* Streamlit
* Environment Variables
* AI application development

---

# 🔮 Future Architecture

A more advanced version of MediBot could evolve into:

```text
                    ┌───────────────┐
                    │ React Frontend│
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │ FastAPI       │
                    │ Backend       │
                    └───────┬───────┘
                            ↓
              ┌─────────────┴─────────────┐
              ↓                           ↓
       Authentication               RAG Pipeline
              ↓                           ↓
          Database                  Vector Database
                                          ↓
                                      LLM API
```

This architecture could allow MediBot to support multiple users, personalized document collections, authentication, chat history, and scalable deployment.

---

# 🤝 Contributing

Contributions are welcome.

### 1. Fork the repository

```bash
git fork
```

### 2. Create a branch

```bash
git checkout -b feature/new-feature
```

### 3. Make your changes

```bash
git add .
git commit -m "Add new feature"
```

### 4. Push your branch

```bash
git push origin feature/new-feature
```

### 5. Create a Pull Request

Describe the changes and improvements included in your contribution.

---

# 📜 License

This project is intended primarily for educational and demonstration purposes.

You may add an appropriate open-source license such as the MIT License depending on how you plan to distribute the project.

---

# 👨‍💻 Author

**Rohan Kumar Pathak**

B.Tech Computer Science Engineering

### Interests

* Full Stack Development
* MERN Stack
* Generative AI
* RAG Systems
* LangChain
* Machine Learning
* Backend Development
* Data Structures & Algorithms

---

# ⭐ Project Highlights

**MediBot combines:**

```text
Python
   +
LangChain
   +
Hugging Face
   +
Sentence Transformers
   +
FAISS
   +
RAG
   +
Streamlit
   =
AI-Powered Medical Information Assistant
```

If you find this project useful, consider giving the repository a ⭐ on GitHub.

---

## ⚠️ Disclaimer

MediBot provides information for **educational and informational purposes only**. It does not provide medical diagnosis, treatment, or professional medical advice. Always consult a qualified healthcare professional for medical concerns, and seek emergency medical assistance when necessary.
