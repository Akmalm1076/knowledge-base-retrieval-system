from sentence_transformers import CrossEncoder

model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank_chunks(query, results):

    pairs = [
        (query, result["chunk_text"])
        for result in results
    ]

    scores = model.predict(pairs)

    ranked_results = sorted(
        zip(results, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        result
        for result, score in ranked_results[:3]
    ]