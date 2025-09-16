from pydantic import BaseModel
from typing import List


class AskRequest(BaseModel):
    """Schema for a question request."""
    question: str


class AskResponse(BaseModel):
    """Schema for the answer returned by the model."""
    answer: str
    sources: List[str] = []


class IngestRequest(BaseModel):
    """Schema for document ingestion request."""
    path: str  # folder path


class Health(BaseModel):
    """Schema for health check response."""
    status: str
