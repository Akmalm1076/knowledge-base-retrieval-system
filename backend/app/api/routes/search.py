from fastapi import APIRouter
from app.services.retrieval_service import search_similar_chunks
from app.services.gemini_service import generate_response

router = APIRouter()

@router.get("/search")
def search(query: str, document: str = None):

    results = search_similar_chunks(query, document)

    context = "\n".join([result[0] for result in results])

    answer = generate_response(query, context)

    return {
        "query": query,
        "document": document,
        "answer": answer,
        "context": [result[0] for result in results]
    }