from fastapi import FastAPI
from app.api.routes.health import router as health_router
from app.api.routes.search import router as search_router
from app.api.routes.upload import router as upload_router
from app.api.routes.documents import router as documents_router
# Entry point of the FastAPI backend application.
# Starts the API server and defines routes/endpoints for interacting with the system.
# This file will later connect frontend requests with the RAG pipeline and database operations.
app = FastAPI()
app.include_router(health_router) 
app.include_router(search_router)
app.include_router(upload_router)
app.include_router(documents_router)
@app.get("/")
def root():
    return {"message": "Knowledge Base Retrieval System Running"}
