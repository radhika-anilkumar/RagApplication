# from pydantic import BaseSettings
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # Vector DB
    chroma_dir: str = "../chroma"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    # LLM configs
    llm_backend: str = "mock"  # ollama | openai | mock
    ollama_model: str = "llama3:latest"
    ollama_base_url: str = "http://localhost:11434"

    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"

    # RAG configs
    chunk_size: int = 1200
    chunk_overlap: int = 150
    top_k: int = 4
    max_tokens: int = 512
    temperature: float = 0.1

    # Server configs
    host: str = "0.0.0.0"
    port: int = 8000


settings = Settings()
