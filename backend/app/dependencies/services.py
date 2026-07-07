from app.services.retrieval_service import search_similar_chunks
from app.services.gemini_service import generate_response
from app.services.reranking_service import rerank_chunks

def get_retrieval_service():
    return search_similar_chunks


def get_gemini_service():
    return generate_response


def get_reranking_service():
    return rerank_chunks