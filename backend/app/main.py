from app.api.routes.health import router as health_router
from app.api.routes.search import router as search_router
from app.api.routes.upload import router as upload_router
from app.api.routes.documents import router as documents_router
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.exceptions import (
    DatabaseException,
    DocumentProcessingException,
    EmbeddingException,
    GeminiException
)
from app.core.logging_config import logger
from fastapi.middleware.cors import CORSMiddleware
# Entry point of the FastAPI backend application.
# Starts the API server and defines routes/endpoints for interacting with the system.
# This file will later connect frontend requests with the RAG pipeline and database operations.
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("Application starting")
@app.exception_handler(DatabaseException)
async def database_exception_handler(
    request: Request,
    exc: DatabaseException
):
    
    logger.error(f"DatabaseException: {str(exc)}")

    return JSONResponse(
        status_code=500,
        content={
            "detail": str(exc)
        }
    )

@app.exception_handler(DocumentProcessingException)
async def document_processing_exception_handler(
    request: Request,
    exc: DocumentProcessingException
):
    
    logger.error(f"DocumentProcessingException: {str(exc)}")

    return JSONResponse(
        status_code=400,
        content={
            "detail": str(exc)
        }
    )


@app.exception_handler(EmbeddingException)
async def embedding_exception_handler(
    request: Request,
    exc: EmbeddingException
):
    
    logger.error(f"EmbeddingException: {str(exc)}")

    return JSONResponse(
        status_code=500,
        content={
            "detail": str(exc)
        }
    )


@app.exception_handler(GeminiException)
async def gemini_exception_handler(
    request: Request,
    exc: GeminiException
):
    
    logger.error(f"GeminiException: {str(exc)}")

    return JSONResponse(
        status_code=500,
        content={
            "detail": str(exc)
        }
    )

app.include_router(
    health_router,
    prefix="/api/v1"
)

app.include_router(
    search_router,
    prefix="/api/v1"
)

app.include_router(
    upload_router,
    prefix="/api/v1"
)

app.include_router(
    documents_router,
    prefix="/api/v1"
)
@app.get("/")
def root():
    return {"message": "Knowledge Base Retrieval System Running"}
