
import json
from pathlib import Path

import faiss
import numpy as np


INDEX_DIR = Path("data/local_index")


def create_vector_store(all_chunks):
    metadata = {}
    embeddings = []

    for i, chunk in enumerate(all_chunks):
        chunk_id = f"chunk_{i:04d}"

        metadata[chunk_id] = {
            "filename": chunk["filename"],
            "file_path": chunk["file_path"],
            "file_type": chunk["file_type"],
            "chunk": chunk["chunk"],
        }

        embeddings.append(chunk["embedding"])

    if not embeddings:
        return None, {}

    embeddings = np.asarray(embeddings, dtype="float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    return index, metadata


def save_vector_store(index, metadata, index_dir=INDEX_DIR):
    if index is None:
        raise ValueError("Cannot save an empty index.")

    index_dir = Path(index_dir)
    index_dir.mkdir(parents=True, exist_ok=True)

    faiss.write_index(index, str(index_dir / "documents.faiss"))

    with open(index_dir / "metadata.json", "w", encoding="utf-8") as file:
        json.dump(metadata, file, ensure_ascii=False)


def load_vector_store(index_dir=INDEX_DIR):
    index_dir = Path(index_dir)

    index_path = index_dir / "documents.faiss"
    metadata_path = index_dir / "metadata.json"

    if not index_path.exists() or not metadata_path.exists():
        return None, {}

    index = faiss.read_index(str(index_path))

    with open(metadata_path, "r", encoding="utf-8") as file:
        metadata = json.load(file)

    if index.ntotal != len(metadata):
        raise ValueError("Index and metadata counts do not match.")

    return index, metadata
