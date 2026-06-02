from app.services.retrieval_service import search_similar_chunks
from app.services.gemini_service import generate_response


def get_retrieval_service():
    return search_similar_chunks


def get_gemini_service():
    return generate_response