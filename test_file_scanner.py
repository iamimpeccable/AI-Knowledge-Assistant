
from utils.file_scanner import scan_local_files

files = scan_local_files()

print(f"\nFound {len(files)} supported files.\n")

for file_path in files[:10]:
    print(file_path)
