from typing import Callable

from fastapi import APIRouter, Depends

from app.core.logging_config import logger
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

    logger.info("=" * 60)
    logger.info("SEARCH EVALUATION")
    logger.info("=" * 60)
    logger.info(f"Query: {request.query}")
    logger.info(f"Document Filter: {request.document or 'All Documents'}")
    logger.info(f"Retrieved Candidates: {len(results)}")

    for index, result in enumerate(results, start=1):

        found_by = []

        if result["found_by"]["semantic"]:
            found_by.append("Semantic")

        if result["found_by"]["keyword"]:
            found_by.append("Keyword")

        logger.info(f"Candidate {index}")
        logger.info(f"  Document        : {result['document_name']}")
        logger.info(f"  Found By        : {', '.join(found_by)}")
        logger.info(f"  Reranker Score  : {result['reranker_score']:.4f}")
        logger.info(f"  Preview         : {result['chunk_text'][:120]}...")
        logger.info("-" * 60)

    context = "\n".join(
        [
            result["chunk_text"]
            for result in results
        ]
    )

    answer = gemini_service(
        request.query,
        context
    )

    logger.info("Gemini response generated successfully.")
    logger.info("=" * 60)

    return {
        "query": request.query,
        "document": request.document,
        "answer": answer,
        "context": results
    }