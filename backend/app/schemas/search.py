from typing import Optional

from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str
    document: Optional[str] = None


class RetrievedContext(BaseModel):
    chunk_text: str
    document_name: str
    found_by: dict[str, bool]
    reranker_score: float


class SearchResponse(BaseModel):
    query: str
    document: Optional[str] = None
    answer: str
    context: list[RetrievedContext]