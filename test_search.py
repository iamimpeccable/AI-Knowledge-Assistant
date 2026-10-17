
from pathlib import Path

from utils.indexer import index_files
from utils.search import search_documents

test_file = Path("test_index_document.txt")

test_file.write_text(
    "FAISS performs similarity search over vectors. "
    "Text embeddings represent the meaning of documents "
    "as numerical values.",
    encoding="utf-8",
)

try:
    index, metadata = index_files([test_file])

    results = search_documents(
        "How does FAISS find relevant text?",
        index,
        metadata,
        top_k=3,
    )

    for result in results:
        print("\nFilename:", result["filename"])
        print("Path:", result["file_path"])
        print("Distance:", result["distance"])
        print("Matching text:", result["chunk"])

finally:
    test_file.unlink(missing_ok=True)
