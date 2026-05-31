class DatabaseException(Exception):
    """Raised when a database operation fails."""
    pass


class DocumentProcessingException(Exception):
    """Raised when document ingestion fails."""
    pass


class EmbeddingException(Exception):
    """Raised when embedding generation fails."""
    pass


class GeminiException(Exception):
    """Raised when Gemini response generation fails."""
    pass