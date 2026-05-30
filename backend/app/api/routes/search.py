from fastapi import APIRouter
from app.services.retrieval_service import search_similar_chunks
from app.services.gemini_service import generate_response
from app.schemas.search import SearchRequest, SearchResponse

router = APIRouter()


@router.post("/search", response_model=SearchResponse)
def search(request: SearchRequest):

    results = search_similar_chunks(
        request.query,
        request.document
    )

    context = "\n".join([result[0] for result in results])

    answer = generate_response(
        request.query,
        context
    )

    return {
        "query": request.query,
        "document": request.document,
        "answer": answer,
        "context": [result[0] for result in results]
    }