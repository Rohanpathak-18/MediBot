from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_huggingface import (
    HuggingFaceEmbeddings
)

from langchain_community.vectorstores import FAISS


# =========================================================
# PROJECT PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parents[2]


# =========================================================
# MAIN VECTORSTORE PATH
# =========================================================

VECTORSTORE_DIR = (
    BASE_DIR /
    "vectorstore" /
    "db_faiss"
)


# =========================================================
# EMBEDDINGS
# =========================================================

def get_embedding_model():

    return HuggingFaceEmbeddings(

        model_name=
        "sentence-transformers/all-MiniLM-L6-v2"

    )


# =========================================================
# LOAD DOCUMENT
# =========================================================

def load_document(
    file_path: str,
    extension: str
):

    extension = extension.lower()


    # -----------------------------------------------------
    # PDF
    # -----------------------------------------------------

    if extension == ".pdf":

        loader = PyPDFLoader(
            file_path
        )


    # -----------------------------------------------------
    # DOCX
    # -----------------------------------------------------

    elif extension == ".docx":

        loader = Docx2txtLoader(
            file_path
        )


    # -----------------------------------------------------
    # TXT
    # -----------------------------------------------------

    elif extension == ".txt":

        loader = TextLoader(
            file_path,
            encoding="utf-8"
        )


    else:

        raise ValueError(
            "Unsupported file type."
        )


    documents = loader.load()


    if not documents:

        raise ValueError(
            "No text could be extracted from the document."
        )


    return documents


# =========================================================
# SPLIT DOCUMENT
# =========================================================

def split_documents(documents):

    text_splitter = RecursiveCharacterTextSplitter(

        chunk_size=500,

        chunk_overlap=50,

        length_function=len

    )


    chunks = text_splitter.split_documents(
        documents
    )


    if not chunks:

        raise ValueError(
            "Document could not be split into chunks."
        )


    return chunks


# =========================================================
# CREATE / UPDATE VECTORSTORE
# =========================================================

def create_vectorstore(
    chunks
):

    embeddings = get_embedding_model()


    # -----------------------------------------------------
    # Make directory
    # -----------------------------------------------------

    VECTORSTORE_DIR.mkdir(

        parents=True,

        exist_ok=True

    )


    # -----------------------------------------------------
    # If existing vectorstore exists,
    # load and add new documents.
    # -----------------------------------------------------

    index_file = (
        VECTORSTORE_DIR /
        "index.faiss"
    )

    pickle_file = (
        VECTORSTORE_DIR /
        "index.pkl"
    )


    if (
        index_file.exists()
        and
        pickle_file.exists()
    ):

        print(
            "Existing FAISS vectorstore found."
        )


        vectorstore = FAISS.load_local(

            str(VECTORSTORE_DIR),

            embeddings,

            allow_dangerous_deserialization=True

        )


        vectorstore.add_documents(
            chunks
        )


    else:

        print(
            "Creating new FAISS vectorstore."
        )


        vectorstore = FAISS.from_documents(

            chunks,

            embeddings

        )


    # -----------------------------------------------------
    # Save vectorstore
    # -----------------------------------------------------

    vectorstore.save_local(

        str(VECTORSTORE_DIR)

    )


    print(
        "FAISS vectorstore saved at:",
        VECTORSTORE_DIR
    )


    return vectorstore


# =========================================================
# PROCESS DOCUMENT
# =========================================================

def process_document(

    file_path: str,

    extension: str,

    document_id: str

):

    print(
        "Processing document:",
        file_path
    )


    # -----------------------------------------------------
    # Load
    # -----------------------------------------------------

    documents = load_document(

        file_path,

        extension

    )


    print(
        "Pages/documents loaded:",
        len(documents)
    )


    # -----------------------------------------------------
    # Add metadata
    # -----------------------------------------------------

    for document in documents:

        document.metadata[
            "document_id"
        ] = document_id


        document.metadata[
            "source_file"
        ] = Path(file_path).name


    # -----------------------------------------------------
    # Split
    # -----------------------------------------------------

    chunks = split_documents(
        documents
    )


    print(
        "Chunks created:",
        len(chunks)
    )


    # -----------------------------------------------------
    # Create vectorstore
    # -----------------------------------------------------

    create_vectorstore(
        chunks
    )


    # -----------------------------------------------------
    # Return result
    # -----------------------------------------------------

    return {

        "document_id": document_id,

        "chunks": len(chunks)

    }