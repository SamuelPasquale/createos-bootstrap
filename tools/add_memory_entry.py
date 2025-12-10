#!/usr/bin/env python3
"""
Tool: add_memory_entry.py
Purpose: Append a structured memory entry to creation/05-memory/memory.md
Creation: C01 – CreateOS Bootstrap
"""

import os
import datetime
import argparse

MEMORY_FILE_PATH = "creation/05-memory/memory.md"


def load_existing_memory():
    if not os.path.exists(MEMORY_FILE_PATH):
        raise FileNotFoundError(f"Memory file not found at: {MEMORY_FILE_PATH}")
    with open(MEMORY_FILE_PATH, "r", encoding="utf-8") as f:
        return f.read()


def append_entry(event, reasoning, changes):
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"

    changes_block = ""
    for c in changes:
        changes_block += f"  - {c}\n"

    new_entry = f"""
### [{timestamp}]
event: {event}
reasoning: {reasoning}
changes:
{changes_block}
"""
    return new_entry


def write_memory_entry(entry_text):
    with open(MEMORY_FILE_PATH, "a", encoding="utf-8") as f:
        f.write(entry_text)


def main():
    parser = argparse.ArgumentParser(description="Append a structured memory entry.")
    parser.add_argument("--event", required=True, help="Short description of what happened.")
    parser.add_argument("--reasoning", required=True, help="Why the action occurred.")
    parser.add_argument(
        "--changes",
        nargs="*",
        default=[],
        help="List of changes (e.g., file_created: X).",
    )

    args = parser.parse_args()

    # Construct entry
    entry = append_entry(
        event=args.event,
        reasoning=args.reasoning,
        changes=args.changes,
    )

    # Write to file
    write_memory_entry(entry)
    print("Memory entry appended successfully.")


if __name__ == "__main__":
    main()
