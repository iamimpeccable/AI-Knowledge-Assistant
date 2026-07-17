import numpy as np
from utils.embeddings import create_embedding

def retrieve_chunks(question, index, metadata, k=3):
    """
    Retrieves the k most similar chunks for a user question.
    """

    # Step 1: Convert question into an embedding
    question_embedding = create_embedding(question)

    # Step 2: Convert to NumPy array
    question_embedding = np.array(
        [question_embedding],
        dtype="float32"
    )

    # Step 3: Search FAISS
    distances, indices = index.search(question_embedding, k)

    # Step 4: Retrieve original chunks
    retrieved_chunks = []

    for idx in indices[0]:

        chunk_id = f"chunk_{idx:04d}"

        retrieved_chunks.append(
            metadata[chunk_id]
        )

    return retrieved_chunks