from typing import Callable

from fastapi import APIRouter, Depends

from app.dependencies.services import (
    get_retrieval_service,
    get_gemini_service,
    get_reranking_service
)
from app.schemas.search import SearchRequest, SearchResponse

router = APIRouter()


@router.post("/search", response_model=SearchResponse)
def search(
    request: SearchRequest,
    retrieval_service: Callable = Depends(
        get_retrieval_service
    ),
    reranking_service: Callable = Depends(
        get_reranking_service
    ),
    gemini_service: Callable = Depends(
        get_gemini_service
    )
):

    results = retrieval_service(
        request.query,
        request.document
    )

    results = reranking_service(
        request.query,
        results
    )

    context = "\n".join(
        [result["chunk_text"] for result in results]
    )

    answer = gemini_service(
        request.query,
        context
    )

    return {
        "query": request.query,
        "document": request.document,
        "answer": answer,
        "context": [
            result["chunk_text"]
            for result in results
        ]
    }