
from utils.file_scanner import scan_local_files
from utils.indexer import index_files


def main():
    print("Scanning for supported documents...")
    files = scan_local_files()

    print(f"Found {len(files)} candidate files.")

    if not files:
        print("No supported files found.")
        return

    print("Extracting, chunking, and embedding documents locally...")
    index, metadata = index_files(files)

    if index is None:
        print("No readable document chunks were indexed.")
        return

    print(f"\nIndexing complete!")
    print(f"Documents indexed: {len(set(item['file_path'] for item in metadata.values()))}")
    print(f"Text chunks indexed: {index.ntotal}")
    print("Saved index: data/local_index/documents.faiss")
    print("Saved metadata: data/local_index/metadata.json")


if __name__ == "__main__":
    main()
