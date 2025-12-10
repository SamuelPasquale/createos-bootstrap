#!/usr/bin/env python3
from __future__ import annotations
import json
import os
import argparse
import datetime
import subprocess
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROGRESS_DIR = os.path.join(REPO_ROOT, "creation", "08-progress")
TASKS_FILE = os.path.join(REPO_ROOT, "creation", "07-tasks", "tasks.json")
MEMORY_SCRIPT = os.path.join(REPO_ROOT, "tools", "add_memory_entry.py")

# Ensure we can import local tools when running from arbitrary working directories
sys.path.insert(0, REPO_ROOT)

# Preferred import helpers (if available)
try:
    from tools.add_memory_entry import append_entry as _append_entry_func
    from tools.add_memory_entry import write_memory_entry as _write_memory_entry_func
except Exception:
    _append_entry_func = None
    _write_memory_entry_func = None

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)
        f.write("\n")


def update_tasks(completed_ids):
    tasks = load_tasks()
    id_map = {t.get("id"): t for t in tasks if isinstance(t, dict) and "id" in t}
    changed = False
    for cid in completed_ids:
        t = id_map.get(cid)
        if t and t.get("status") != "complete":
            t["status"] = "complete"
            changed = True
    if changed:
        save_tasks(list(id_map.values()))


def _format_changes_for_memory(changes):
    formatted = []
    completed = changes.get("completed") or []
    next_steps = changes.get("next_steps") or []
    if completed:
        formatted.append("completed: " + ", ".join(completed))
    if next_steps:
        formatted.append("next_steps: " + ", ".join(next_steps))
    return formatted if formatted else ["no changes recorded"]


def append_memory_entry(date_iso, summary, changes):
    entry = {
        "timestamp": date_iso,
        "event": "session_close",
        "reasoning": summary,
        "changes": changes,
    }

    # Attempt import-based call first (preferred)
    try:
        if _append_entry_func and _write_memory_entry_func:
            change_items = _format_changes_for_memory(changes)
            try:
                entry_text = _append_entry_func(event="session_close", reasoning=summary, changes=change_items)
            except TypeError:
                # fallback if signature differs: call with positional args
                entry_text = _append_entry_func("session_close", summary, change_items)
            try:
                _write_memory_entry_func(entry_text)
            except Exception:
                # If write helper expects the raw object, call with object
                _write_memory_entry_func(entry)
            return True
    except Exception as e:
        print("Warning: import-based memory append failed:", e, file=sys.stderr)

    # CLI fallback: use add_memory_entry.py with explicit flags
    try:
        subprocess.run(
            [
                sys.executable,
                MEMORY_SCRIPT,
                "--event",
                "session_close",
                "--reasoning",
                summary,
                "--changes",
                json.dumps(changes),
            ],
            check=True,
        )
    # CLI fallback: pass JSON as single argument
    try:
        subprocess.run([sys.executable, MEMORY_SCRIPT, json.dumps(entry)], check=True)
        return True
    except Exception as e:
        print("Warning: CLI memory append failed:", e, file=sys.stderr)
        return False


def write_progress_file(date, summary, completed, next_steps, sha):
    ensure_dir(PROGRESS_DIR)
    filename = f"{date}.md"
    filepath = os.path.join(PROGRESS_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# Progress Log — {date}\n\n")
        f.write("## Summary of Work Completed\n\n")
        f.write(f"- {summary}\n\n")
        if completed:
            f.write("## Completed Tasks\n\n")
            for c in completed:
                f.write(f"- {c}\n")
            f.write("\n")
        if next_steps:
            f.write("## Next Steps\n\n")
            for n in next_steps:
                f.write(f"- {n}\n")
            f.write("\n")
        if sha:
            f.write("## Commit\n\n")
            f.write(f"- HEAD SHA: {sha}\n")
    return filepath, filename


def write_latest_json(date, filename, sha, summary, next_steps):
    latest = {
        "date": date,
        "file": filename,
        "sha": sha or "",
        "summary": summary,
        "next_steps": next_steps,
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
    }
    latest_path = os.path.join(PROGRESS_DIR, "LATEST.json")
    with open(latest_path, "w", encoding="utf-8") as f:
        json.dump(latest, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return latest_path


def parse_csv(s):
    if not s:
        return []
    return [i.strip() for i in s.split(",") if i.strip()]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=False, help="YYYY-MM-DD")
    parser.add_argument("--summary", required=True)
    parser.add_argument("--completed", required=False, help="comma-separated task ids")
    parser.add_argument("--next", required=False, help="comma-separated next-step task ids")
    parser.add_argument("--sha", required=False, help="HEAD SHA for reference")
    args = parser.parse_args()

    date = args.date or datetime.date.today().isoformat()
    completed = parse_csv(args.completed)
    next_steps = parse_csv(args.next)

    progress_path, filename = write_progress_file(date, args.summary, completed, next_steps, args.sha)
    latest_path = write_latest_json(date, f"creation/08-progress/{filename}", args.sha or "", args.summary, next_steps)

    if completed:
        update_tasks(completed)

    appended = append_memory_entry(datetime.datetime.utcnow().isoformat() + "Z", args.summary, {"completed": completed, "next_steps": next_steps})

    print("Session closed.")
    print("Progress file:", progress_path)
    print("LATEST.json updated at", latest_path)
    print("Memory append successful:", appended)


if __name__ == "__main__":
    main()
