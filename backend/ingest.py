import os
ingest_path = os.path.join(os.getcwd(), "data")  # or wherever your PDFs/text files are
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from .settings import settings
from .utils import make_text_splitter


def ingest_file(file_path: str):
    # Choose loader based on extension
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext in [".txt", ".md"]:
        loader = TextLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    docs = loader.load()
    splitter = make_text_splitter()
    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(model_name=settings.embedding_model)

    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=settings.chroma_dir,
    )

    db.persist()
    return len(chunks)
