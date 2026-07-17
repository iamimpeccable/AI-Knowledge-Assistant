from pathlib import Path

def load_documents(folder_path="data/documents"):
    documents = []

    # Get all .txt files
    for file in Path(folder_path).glob("*.txt"):
        with open(file, "r", encoding="utf-8") as f:
            text = f.read()

            documents.append({
                "filename": file.name,
                "content": text
            })

    return documents