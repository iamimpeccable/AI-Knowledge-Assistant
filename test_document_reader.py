
from utils.file_scanner import scan_local_files
from utils.document_reader import extract_text

files = scan_local_files()
tested_extensions = set()

for file_path in files:
    extension = file_path.suffix.lower()

    if extension in tested_extensions:
        continue

    try:
        text = extract_text(file_path)

        print(f"\nFile type: {extension}")
        print(f"Filename: {file_path.name}")
        print(f"Characters extracted: {len(text)}")
        print(f"Preview: {text[:150]!r}")

        tested_extensions.add(extension)

    except Exception as error:
        print(f"\nFailed to read {file_path.name}: {error}")

    if len(tested_extensions) == 3:
        break

print("\nSuccessfully tested:", tested_extensions)
