from fastapi import APIRouter
from app.db.database import cursor

router = APIRouter()

@router.get("/documents")
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