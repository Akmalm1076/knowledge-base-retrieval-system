from fastapi import APIRouter
from app.db.database import cursor
from app.schemas.documents import DocumentsResponse

router = APIRouter()


@router.get("/documents", response_model=DocumentsResponse)
def list_documents():

    cursor.execute(
        """
        SELECT DISTINCT document_name
        FROM document_chunks
        ORDER BY document_name;
        """
    )

    documents = cursor.fetchall()

    return {
        "documents": [document[0] for document in documents]
    }