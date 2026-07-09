from app.db.database import cursor
from app.services.embedding_service import generate_embedding
from app.exceptions import DatabaseException
from app.core.logging_config import logger


# Retrieves the most semantically similar text chunks from PostgreSQL
# Uses hybrid retrieval (semantic + keyword)
# Returns structured retrieval objects with provenance information.
def search_similar_chunks(query, document_name=None):

    if document_name:
        logger.info(
            f"Starting retrieval for query against document: {document_name}"
        )
    else:
        logger.info(
            "Starting retrieval across all documents"
        )

    query_embedding = generate_embedding(query)

    try:

        if document_name:

            cursor.execute(
                """
                SELECT
                    chunk_text,
                    document_name,
                    BOOL_OR(found_by_semantic) AS found_by_semantic,
                    BOOL_OR(found_by_keyword) AS found_by_keyword
                FROM
                (
                    (
                        SELECT
                            chunk_text,
                            document_name,
                            TRUE AS found_by_semantic,
                            FALSE AS found_by_keyword
                        FROM document_chunks
                        WHERE document_name = %s
                        ORDER BY embedding <-> %s::vector
                        LIMIT 20
                    )

                    UNION ALL

                    (
                        SELECT
                            chunk_text,
                            document_name,
                            FALSE AS found_by_semantic,
                            TRUE AS found_by_keyword
                        FROM document_chunks
                        WHERE
                            to_tsvector('english', chunk_text)
                            @@ plainto_tsquery('english', %s)
                            AND document_name = %s
                        LIMIT 20
                    )
                ) AS combined_results
                GROUP BY
                    chunk_text,
                    document_name
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
                SELECT
                    chunk_text,
                    document_name,
                    BOOL_OR(found_by_semantic) AS found_by_semantic,
                    BOOL_OR(found_by_keyword) AS found_by_keyword
                FROM
                (
                    (
                        SELECT
                            chunk_text,
                            document_name,
                            TRUE AS found_by_semantic,
                            FALSE AS found_by_keyword
                        FROM document_chunks
                        ORDER BY embedding <-> %s::vector
                        LIMIT 20
                    )

                    UNION ALL

                    (
                        SELECT
                            chunk_text,
                            document_name,
                            FALSE AS found_by_semantic,
                            TRUE AS found_by_keyword
                        FROM document_chunks
                        WHERE
                            to_tsvector('english', chunk_text)
                            @@ plainto_tsquery('english', %s)
                        LIMIT 20
                    )
                ) AS combined_results
                GROUP BY
                    chunk_text,
                    document_name
                LIMIT 20;
                """,
                (
                    query_embedding,
                    query
                )
            )

        rows = cursor.fetchall()

        retrieval_results = [
            {
                "chunk_text": row[0],
                "document_name": row[1],
                "found_by": {
                    "semantic": row[2],
                    "keyword": row[3]
                }
            }
            for row in rows
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