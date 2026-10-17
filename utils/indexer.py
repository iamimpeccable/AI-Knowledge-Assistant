
from pathlib import Path

from utils.chunker import chunk_text
from utils.document_reader import extract_text
from utils.embeddings import create_embedding
from vector_store.vector_store import create_vector_store


def index_files(file_paths):
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

        chunks = chunk_text(text)

        for chunk in chunks:
            try:
                embedding = create_embedding(chunk)
            except Exception as error:
                print(f"Embedding failed for {file_path.name}: {error}")
                continue

            all_chunks.append({
                "filename": file_path.name,
                "file_path": str(file_path.resolve()),
                "file_type": file_path.suffix.lower(),
                "chunk": chunk,
                "embedding": embedding,
            })

    if not all_chunks:
        return None, {}

    return create_vector_store(all_chunks)
