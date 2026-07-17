import faiss
import numpy as np

def create_vector_store(all_chunks):
    # -----------------------------
    # Metadata Store
    # -----------------------------

    metadata = {}

    embeddings =[]

    # Generate our own IDs
    for i, chunk in enumerate(all_chunks):

        chunk_id = f"chunk_{i:04d}"

        metadata[chunk_id] = {
            "filename": chunk["filename"],
            "chunk": chunk["chunk"]
        }

        embeddings.append(chunk["embedding"])

    # -----------------------------
    # Create FAISS Index
    # -----------------------------

    dimension = len(embeddings[0])
    index = faiss.IndexFlatL2(dimension)
    embeddings = np.array(embeddings).astype("float32")
    index.add(embeddings)

    return index, metadata 