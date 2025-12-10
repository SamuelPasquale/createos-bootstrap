# tools/refresh_index.py
import os
import json
from datetime import datetime

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

IGNORE_DIRS = {
    ".git",
    ".idea",
    "__pycache__",
    ".venv",
    ".mypy_cache",
    ".pytest_cache",
    ".createos",  # we will write index into this but still track it explicitly
}

IGNORE_FILES = {
    # add anything large or irrelevant if needed
}

def build_index(root: str) -> dict:
    files = []

    for dirpath, dirnames, filenames in os.walk(root):
        # Normalize dirnames in-place to skip ignored directories
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]

        for name in filenames:
            if name in IGNORE_FILES:
                continue
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root).replace("\\", "/")
            files.append(rel)

    files.sort()
    return {
        "generated_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "root": ".",
        "file_count": len(files),
        "files": files,
    }

def main():
    index = build_index(REPO_ROOT)
    out_dir = os.path.join(REPO_ROOT, ".createos")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "index.json")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

    print(f"Wrote {index['file_count']} paths to .createos/index.json")

if __name__ == "__main__":
    main()
