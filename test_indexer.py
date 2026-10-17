
from pathlib import Path

from utils.indexer import index_files

# Create a small temporary document for testing.
test_file = Path("test_index_document.txt")
test_file.write_text(
    "FAISS is a library for efficient similarity search "
    "over dense vectors. Embeddings represent text as "
    "numerical vectors that help retrieve relevant documents.",
    encoding="utf-8",
)

try:
    index, metadata = index_files([test_file])

    if index is None:
        print("No chunks were indexed.")
    else:
        print("Indexing successful!")
        print("Number of vectors:", index.ntotal)
        print("Number of metadata entries:", len(metadata))

        first_entry = next(iter(metadata.values()))
        print("Filename:", first_entry["filename"])
        print("File path:", first_entry["file_path"])
        print("File type:", first_entry["file_type"])
        print("Chunk preview:", first_entry["chunk"][:100])

finally:
    test_file.unlink(missing_ok=True)
