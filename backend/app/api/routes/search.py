from typing import Callable

from fastapi import APIRouter, Depends

from app.dependencies.services import (
    get_retrieval_service,
    get_gemini_service
)
from app.schemas.search import SearchRequest, SearchResponse

router = APIRouter()


@router.post("/search", response_model=SearchResponse)
def search(
    request: SearchRequest,
    retrieval_service: Callable = Depends(
        get_retrieval_service
    ),
    gemini_service: Callable = Depends(
        get_gemini_service
    )
):

    results = retrieval_service(
        request.query,
        request.document
    )

    context = "\n".join(
        [result[0] for result in results]
    )

    answer = gemini_service(
        request.query,
        context
    )

    return {
        "query": request.query,
        "document": request.document,
        "answer": answer,
        "context": [result[0] for result in results]
    }