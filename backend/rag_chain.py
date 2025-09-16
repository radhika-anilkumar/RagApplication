# backend/rag_chain.py
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.chat_models import ChatOllama   # ✅ new import path
from langchain.chains import RetrievalQA

def make_chain(persist_dir="./chroma_store", embedding_function=None):
    if embedding_function is None:
        embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vectorstore = Chroma(
        persist_directory=persist_dir,
        embedding_function=embedding_function,
    )

    # ✅ use ChatOllama with llama3
    llm = ChatOllama(model="llama3")

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        return_source_documents=True,
    )

    return qa
