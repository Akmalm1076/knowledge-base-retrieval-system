from fastapi import FastAPI
from app.rag_pipeline import search_similar_chunks
from app.gemini_service import generate_response
from fastapi import UploadFile, File
import os
from app.ingest import ingest_document
from app.database import cursor
# Entry point of the FastAPI backend application.
# Starts the API server and defines routes/endpoints for interacting with the system.
# This file will later connect frontend requests with the RAG pipeline and database operations.
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Knowledge Base Retrieval System Running"}
@app.get("/search")
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
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    # Create file path
    file_path = f"data/{file.filename}"

    # Save uploaded file
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Ingest uploaded PDF
    ingest_document(file_path, file.filename)

    return {
        "message": f"{file.filename} uploaded and processed successfully"
    }
@app.get("/documents")
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