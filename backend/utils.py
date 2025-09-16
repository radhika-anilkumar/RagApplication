# backend/utils.py
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from .settings import settings


def make_text_splitter():
    """Create a text splitter for chunking documents."""
    return RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )


def load_vectorstore():
    """Load Chroma vector store from disk."""
    embeddings = HuggingFaceEmbeddings(model_name=settings.embedding_model)
    return Chroma(
        persist_directory=settings.chroma_dir,
        embedding_function=embeddings
    )


def format_sources(sources):
    """Format retrieved sources for API responses."""
    formatted = []
    for doc in sources:
        formatted.append({
            "content": doc.page_content,
            "metadata": doc.metadata
        })
    return formatted
