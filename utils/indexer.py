
from pathlib import Path

from utils.chunker import chunk_text
from utils.document_reader import extract_text
from utils.embeddings import create_embeddings
from vector_store.vector_store import (
    create_vector_store,
    save_vector_store,
)


def index_files(file_paths, index_dir="data/local_index"):
    all_chunks = []

    for file_path in file_paths:
        file_path = Path(file_path)

        try:
            text = extract_text(file_path)
        except Exception as error:
            print(f"Skipping {file_path.name}: {error}")
            continue

        if not text.strip():
            continue

        for chunk in chunk_text(text):
            all_chunks.append({
                "filename": file_path.name,
                "file_path": str(file_path.resolve()),
                "file_type": file_path.suffix.lower(),
                "chunk": chunk,
            })

    if not all_chunks:
        return None, {}

    texts = [item["chunk"] for item in all_chunks]
    embeddings = create_embeddings(texts, batch_size=32)

    for item, embedding in zip(all_chunks, embeddings):
        item["embedding"] = embedding

    index, metadata = create_vector_store(all_chunks)

    save_vector_store(index, metadata, index_dir)

    return index, metadata
