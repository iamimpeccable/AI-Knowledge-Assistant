
import os
from pathlib import Path

SUPPORTED_EXTENSIONS = {".txt", ".pdf", ".docx"}

EXCLUDED_DIRECTORIES = {
    # Development and cache folders
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".cache",
    ".vscode",
    ".vscode-insiders",
    ".windsurf",
    ".p2",
    "CascadeProjects",

    # Windows and application folders
    "Windows",
    "Program Files",
    "Program Files (x86)",
    "ProgramData",
    "$Recycle.Bin",
    "System Volume Information",
    "Recovery",
    "PerfLogs",
    "AppData",
    "Lib",
    "site-packages",
    "Scripts",

    # Existing exclusions
    ".cisco",
    "Cookies",
    "Local Settings",
    "NetHood",
    "PrintHood",
    "Recent",
    "SendTo",
    "Start Menu",
    "Templates",
    "Application Data",
}

def scan_local_files():
    root_path = Path.home()
    found_files = []
    print("Home directory:", Path.home())
    print("Desktop exists:", (Path.home() / "Desktop").exists())
    print("Prosense folder exists:", (Path.home() / "Desktop" / "Prosense").exists())

    def handle_walk_error(error):
        # Ignore folders Windows does not allow us to access.
        pass

    for current_path, directories, filenames in os.walk(
        root_path,
        onerror=handle_walk_error,
    ):
        # Do not enter excluded folders.
        excluded_lower = {
            directory.lower() for directory in EXCLUDED_DIRECTORIES
        }
        directories[:] = [
            directory
            for directory in directories
            if directory.lower() not in excluded_lower
        ]

        for filename in filenames:
            file_path = Path(current_path) / filename

            if file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
                found_files.append(file_path)
    
    for file in found_files:
        if "prosense" in str(file).lower():
            print("Found Prosense file:", file)
    return found_files
