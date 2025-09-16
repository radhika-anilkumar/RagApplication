# backend/api.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from backend.rag_chain import make_chain
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings   # ✅ fixed import

import shutil
import os


UPLOAD_DIR = "./uploaded_docs"
VECTORSTORE_DIR = "./chroma_store"

os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a global embedding function (not tied to make_chain)
embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# ---- UPLOAD ENDPOINT ----
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Load file
    if file.filename.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path, encoding="utf-8")

    documents = loader.load()

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = splitter.split_documents(documents)

    # Store in Chroma
    vectorstore = Chroma.from_documents(
        docs,
        embedding=embedding_function,   # ✅ FIXED
        persist_directory=VECTORSTORE_DIR,
    )
    vectorstore.persist()

    return {"message": f"Uploaded and indexed {file.filename}"}


    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = splitter.split_documents(documents)

    # Store in Chroma
    vectorstore = Chroma.from_documents(
        docs,
        embedding_function=embedding_function,
        persist_directory=VECTORSTORE_DIR,
    )
    vectorstore.persist()

    return {"message": f"Uploaded and indexed {file.filename}"}

# ---- ASK ENDPOINT ----
@app.post("/ask")
async def ask_question(payload: dict):
    query = payload.get("query")
    if not query:
        return {"error": "No query provided"}

    rag_chain = make_chain(persist_dir=VECTORSTORE_DIR, embedding_function=embedding_function)
    result = rag_chain.invoke({"query": query})
    return {"answer": result["result"]}
