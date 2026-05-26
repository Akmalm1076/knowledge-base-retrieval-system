from app.db.database import cursor
from app.services.embedding_service import generate_embedding
# Retrieves the most semantically similar text chunks from PostgreSQL
# Converts user query into an embedding vector and compares it against stored embeddings
# Uses pgvector similarity search to return the closest matching chunks
def search_similar_chunks(query, document_name=None):

    # Generate embedding for semantic search
    query_embedding = generate_embedding(query)

    # Hybrid retrieval:
    # 1. Semantic vector similarity
    # 2. Keyword text matching
        # Optional document filtering
        # Optional document filtering
    document_filter = ""

    if document_name:

        document_filter = "WHERE document_name = %s"

        cursor.execute(
            f"""
            SELECT DISTINCT chunk_text
            FROM
            (
                (
                    SELECT chunk_text
                    FROM document_chunks
                    {document_filter}
                    ORDER BY embedding <-> %s::vector
                    LIMIT 3
                )

                UNION

                (
                    SELECT chunk_text
                    FROM document_chunks
                    WHERE to_tsvector('english', chunk_text)
                    @@ plainto_tsquery('english', %s)
                    AND document_name = %s
                    LIMIT 3
                )
            ) AS combined_results
            LIMIT 3;
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
            SELECT DISTINCT chunk_text
            FROM
            (
                (
                    SELECT chunk_text
                    FROM document_chunks
                    ORDER BY embedding <-> %s::vector
                    LIMIT 3
                )

                UNION

                (
                    SELECT chunk_text
                    FROM document_chunks
                    WHERE to_tsvector('english', chunk_text)
                    @@ plainto_tsquery('english', %s)
                    LIMIT 3
                )
            ) AS combined_results
            LIMIT 3;
            """,
            (
                query_embedding,
                query
            )
        )

    results = cursor.fetchall()

    return results


if __name__ == "__main__":

    query = "What programming languages does Akmal know?"

    results = search_similar_chunks(query)

    for result in results:
        print(result[0])