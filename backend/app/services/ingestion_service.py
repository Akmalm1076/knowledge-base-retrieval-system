from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.services.embedding_service import generate_embedding
from app.db.database import cursor, connection
from app.core.config import settings
from app.exceptions import (
    DocumentProcessingException,
    DatabaseException
)
from app.core.logging_config import logger
# Handles the document ingestion pipeline for the knowledge base system.
# Reads PDFs, splits them into smaller chunks, generates embeddings, and stores them in the database.
# This file connects document processing with vector storage.

def load_pdf(file_path):

    try:

        reader = PdfReader(file_path)
        logger.info(f"Successfully loaded PDF: {file_path}")
        text = ""

        for page in reader.pages:
            text += page.extract_text()

        return text

    except Exception as e:
        raise DocumentProcessingException(
            f"Failed to process PDF: {str(e)}"
        )


def split_text(text):

    splitter = RecursiveCharacterTextSplitter(
    chunk_size=settings.CHUNK_SIZE,
    chunk_overlap=settings.CHUNK_OVERLAP,
    separators=["\n\n", "\n", ".", " "]
)
    chunks = splitter.split_text(text)
    logger.info(f"Generated {len(chunks)} chunks")
    return chunks
# Stores text chunks and their corresponding embedding vectors into PostgreSQL.
# Each chunk is converted into a semantic embedding before being inserted into the document_chunks table.
# This function connects the text processing pipeline with the vector database storage system.
def store_chunks(chunks, document_name):

    try:

        # Delete old chunks for the same document
        cursor.execute(
        """
        DELETE FROM document_chunks
        WHERE document_name = %s
        """,
        (document_name,)
        )

        for chunk in chunks:

            # Generate embedding vector
            embedding = generate_embedding(chunk)

            # Insert into PostgreSQL
            cursor.execute(
                """
                INSERT INTO document_chunks
                (document_name, chunk_text, embedding)
                VALUES (%s, %s, %s)
                """,
                (document_name, chunk, embedding)
            )

        # Save all inserted rows
        connection.commit()

        logger.info(
            f"Stored {len(chunks)} chunks for document: {document_name}"
        )

    except Exception as e:
        raise DatabaseException(
            f"Failed to store document chunks: {str(e)}"
        )

# Complete ingestion workflow for a single document.
# Loads PDF text, splits it into chunks, generates embeddings,
# and stores the processed chunks into PostgreSQL.
def ingest_document(file_path, document_name):

    logger.info(
    f"Starting ingestion for document: {document_name}"
    )

    # Load PDF text
    text = load_pdf(file_path)

    # Split text into chunks
    chunks = split_text(text)

    # Store chunks and embeddings
    store_chunks(chunks, document_name)

    logger.info(
        f"Completed ingestion for document: {document_name}"
    )
    
#manual testing code for the entire ingestion pipeline
if __name__ == "__main__":

    ingest_document("data/DataAkmal.pdf", "DataAkmal.pdf")