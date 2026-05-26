from sentence_transformers import SentenceTransformer
# Responsible for converting text chunks into vector embeddings using a transformer model.
# These embeddings are numerical representations of text used for semantic search.
# The generated vectors will later be stored inside PostgreSQL using pgvector.

model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(text):

    embedding = model.encode(text)

    return embedding.tolist()

#testing code for embedding generation
#sample = generate_embedding("This is my first embedding")
#print(len(sample))
#print(sample[:5])