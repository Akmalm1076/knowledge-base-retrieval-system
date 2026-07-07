from app.db.database import cursor
from app.services.embedding_service import generate_embedding
from app.exceptions import DatabaseException
from app.core.logging_config import logger


# Retrieves the most semantically similar text chunks from PostgreSQL
# Converts user query into an embedding vector and compares it against stored embeddings
# Uses hybrid retrieval (semantic + keyword) and returns structured retrieval objects
def search_similar_chunks(query, document_name=None):

    if document_name:
        logger.info(
            f"Starting retrieval for query against document: {document_name}"
        )
    else:
        logger.info(
            "Starting retrieval across all documents"
        )

    # Generate embedding for semantic search
    query_embedding = generate_embedding(query)

    try:

        if document_name:

            cursor.execute(
                """
                SELECT DISTINCT chunk_text, document_name
                FROM
                (
                    (
                        SELECT chunk_text, document_name
                        FROM document_chunks
                        WHERE document_name = %s
                        ORDER BY embedding <-> %s::vector
                        LIMIT 20
                    )

                    UNION

                    (
                        SELECT chunk_text, document_name
                        FROM document_chunks
                        WHERE to_tsvector('english', chunk_text)
                              @@ plainto_tsquery('english', %s)
                        AND document_name = %s
                        LIMIT 20
                    )
                ) AS combined_results
                LIMIT 20;
                """,
                (
                    document_name,
                    query_embedding,
                    query,
                    document_name
                )
            )

        else:

            cursor.execute(
                """
                SELECT DISTINCT chunk_text, document_name
                FROM
                (
                    (
                        SELECT chunk_text, document_name
                        FROM document_chunks
                        ORDER BY embedding <-> %s::vector
                        LIMIT 20
                    )

                    UNION

                    (
                        SELECT chunk_text, document_name
                        FROM document_chunks
                        WHERE to_tsvector('english', chunk_text)
                              @@ plainto_tsquery('english', %s)
                        LIMIT 20
                    )
                ) AS combined_results
                LIMIT 20;
                """,
                (
                    query_embedding,
                    query
                )
            )

        results = cursor.fetchall()

        retrieval_results = [
            {
                "chunk_text": row[0],
                "document_name": row[1]
            }
            for row in results
        ]

        logger.info(
            f"Retrieved {len(retrieval_results)} relevant chunks"
        )

        return retrieval_results

    except Exception as e:
        raise DatabaseException(
            f"Failed to retrieve document chunks: {str(e)}"
        )


if __name__ == "__main__":

    query = "What programming languages does Akmal know?"

    results = search_similar_chunks(query)

    for result in results:
        print(result)