
from utils.embeddings import create_embedding


def search_documents(question, index, metadata, top_k=5):
    if index is None or index.ntotal == 0:
        return []

    # Convert the question into an embedding.
    question_embedding = create_embedding(question)

    # Search FAISS for the closest vectors.
    distances, indices = index.search(
        __import__("numpy").array(
            [question_embedding], dtype="float32"
        ),
        min(top_k, index.ntotal),
    )

    results = []

    for distance, position in zip(distances[0], indices[0]):
        if position < 0:
            continue

        chunk_id = f"chunk_{position:04d}"

        if chunk_id not in metadata:
            continue

        result = metadata[chunk_id].copy()
        result["distance"] = float(distance)
        results.append(result)

    return results
