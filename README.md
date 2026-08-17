# 🩺 MediBot — RAG-Powered Medical Information Assistant

MediBot is an **AI-powered medical information assistant** built using **Retrieval-Augmented Generation (RAG)**. It allows users to ask questions and receive answers based on information retrieved from a provided medical knowledge base.

The project combines **LangChain, Hugging Face models, vector embeddings, and Streamlit** to create an interactive question-answering system.

> ⚠️ **Disclaimer:** MediBot is an educational/research project and is **not a replacement for a qualified doctor or medical professional**. Do not use its responses for diagnosis, treatment, or emergency medical decisions.

---

## 🚀 Features

* 🤖 AI-powered medical question answering
* 📚 Retrieval-Augmented Generation (RAG)
* 🔎 Semantic search over medical documents
* 🧠 Embedding-based document retrieval
* 💬 Interactive chatbot interface
* ⚡ Streamlit-based web application
* 🔐 Environment-variable based API configuration
* 📄 Custom medical knowledge base support
* 🧩 Modular project architecture
* 🌐 Deployable as a web application

---

## 🧠 How MediBot Works

MediBot follows a typical **RAG pipeline**:

```text
                 Medical Documents
                        │
                        ▼
                Document Loader
                        │
                        ▼
                 Text Splitting
                        │
                        ▼
              Text Embeddings
                        │
                        ▼
                Vector Database
                        │
                        │
User Question ─────────┘
        │
        ▼
   Similarity Search
        │
        ▼
 Relevant Documents
        │
        ▼
      LLM
        │
        ▼
 Generated Answer
        │
        ▼
    Streamlit UI
```

Instead of asking the language model to answer entirely from its pretrained knowledge, MediBot first retrieves relevant information from the knowledge base and provides that context to the model.

---

## 🛠️ Tech Stack

### Frontend / UI

* **Streamlit**

### AI / Machine Learning

* **Python**
* **LangChain**
* **Hugging Face**
* **Transformers**
* **Sentence Transformers**
* **Vector Embeddings**

### Retrieval

* **Vector Database**
* Semantic Similarity Search
* Retrieval-Augmented Generation (RAG)

### Development Tools

* Git
* GitHub
* VS Code
* Python Virtual Environment

---

## 📂 Project Structure

```text
MediBot/
│
├── data/
│   └── medical_documents/
│
├── db/
│   └── vector_store/
│
├── medibot.py
│
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

> The exact structure may vary depending on the vector database and document-processing implementation.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/medibot.git
cd medibot
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

### Windows

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

---

## 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the root directory:

```env
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token
```

Add any other API keys required by your selected model or services.

### Important

Never commit your `.env` file to GitHub.

Add it to `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
```

---

## ▶️ Run the Application

Start the Streamlit application using:

```bash
streamlit run medibot.py
```

The application will start locally and provide a URL similar to:

```text
http://localhost:8501
```

Open the URL in your browser to interact with MediBot.

---

## 🔍 RAG Pipeline

MediBot implements the following major RAG components:

### 1. Document Loading

Medical documents are loaded into the application and converted into a format that can be processed by the retrieval pipeline.

### 2. Text Splitting

Large documents are divided into smaller chunks.

This makes it easier for the retrieval system to find the most relevant information.

### 3. Embeddings

Each document chunk is converted into a numerical vector representation using an embedding model.

Conceptually:

```text
Medical Text
     ↓
Embedding Model
     ↓
Vector Representation
```

### 4. Vector Storage

The generated embeddings are stored in a vector database.

This allows MediBot to efficiently perform semantic similarity searches.

### 5. Retrieval

When the user asks a question, MediBot converts the question into an embedding and searches for the most relevant document chunks.

```text
Question
   ↓
Question Embedding
   ↓
Similarity Search
   ↓
Relevant Context
```

### 6. Generation

The retrieved context is passed to the language model along with the user's question.

The model then generates a response based on the available context.

---

## 💬 Example Questions

Users can ask questions such as:

```text
What are the common symptoms of diabetes?

What are the risk factors mentioned in the knowledge base?

What lifestyle changes are commonly recommended?

What does the provided document say about hypertension?
```

The answers are generated using information retrieved from the configured knowledge base.

---

## 🎯 Why RAG?

A normal LLM can generate answers using information learned during training.

However, RAG provides an additional layer:

```text
Traditional LLM

Question
   ↓
LLM
   ↓
Answer
```

With RAG:

```text
Question
   ↓
Retriever
   ↓
Relevant Knowledge
   ↓
LLM + Retrieved Context
   ↓
Answer
```

This can help the application provide answers that are more closely grounded in the provided documents.

---

## 🧩 Key Concepts Demonstrated

This project demonstrates practical knowledge of:

* Generative AI
* Large Language Models
* Retrieval-Augmented Generation
* Prompt Engineering
* LangChain
* Hugging Face
* Embeddings
* Vector Databases
* Semantic Search
* Document Chunking
* Similarity Search
* Python
* Streamlit
* Environment Variables
* AI Application Deployment

---

## 📈 Future Improvements

Potential improvements include:

* [ ] Add conversation memory
* [ ] Add multiple document formats
* [ ] Improve document chunking
* [ ] Add source citations to answers
* [ ] Add confidence/relevance indicators
* [ ] Add authentication
* [ ] Add chat history
* [ ] Add a production vector database
* [ ] Add medical document upload
* [ ] Improve UI/UX
* [ ] Add evaluation metrics for RAG responses
* [ ] Deploy the application publicly
* [ ] Add guardrails for unsafe medical queries

---

## ⚠️ Medical Safety Disclaimer

MediBot is intended **only for educational and informational purposes**.

The generated responses may contain inaccuracies or incomplete information. MediBot should not be used to:

* Diagnose medical conditions
* Prescribe medication
* Replace professional medical advice
* Make emergency medical decisions
* Determine an individual's treatment plan

For medical concerns, users should consult a qualified healthcare professional.

---

## 👨‍💻 Author

**Rohan Kumar Pathak**

Computer Science Engineering Student
Interested in **Software Development, Backend Development, AI/ML, and Generative AI**.

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

---

## 📜 License

This project is intended for educational and research purposes. Add an appropriate open-source license if you plan to distribute the project publicly.
