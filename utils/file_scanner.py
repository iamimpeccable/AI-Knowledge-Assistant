
import os
from pathlib import Path

SUPPORTED_EXTENSIONS = {".txt", ".pdf", ".docx"}

EXCLUDED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "AppData",
    ".cache",
    ".cisco",
    ".p2",
    ".vscode",
    ".vscode-insiders",
    "__pycache__",
    "Cookies",
    "Local Settings",
    "NetHood",
    "PrintHood",
    "Recent",
    "SendTo",
    "Start Menu",
    "Templates",
    "Application Data",
    ".windsurf",
    "CascadeProjects",
}

def scan_local_files():
    root_path = Path.home()
    found_files = []

    def handle_walk_error(error):
        # Ignore folders Windows does not allow us to access.
        pass

    for current_path, directories, filenames in os.walk(
        root_path,
        onerror=handle_walk_error,
    ):
        # Do not enter excluded folders.
        directories[:] = [
            directory
            for directory in directories
            if directory not in EXCLUDED_DIRECTORIES
        ]

        for filename in filenames:
            file_path = Path(current_path) / filename

            if file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
                found_files.append(file_path)

    return found_files
