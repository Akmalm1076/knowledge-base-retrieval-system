from pydantic import BaseModel
from typing import Optional


class SearchRequest(BaseModel):
    query: str
    document: Optional[str] = None


class SearchResponse(BaseModel):
    query: str
    document: Optional[str] = None
    answer: str
    context: list[str]