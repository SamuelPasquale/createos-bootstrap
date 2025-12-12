#!/usr/bin/env python3
"""
Tool: start_session.py
Purpose: Generate a session boot report for CreateOS V0.5 Architect sessions
Creation: C01 – CreateOS Bootstrap
"""

from __future__ import annotations
import json
import os
import argparse
import datetime
import subprocess
import sys
import random
import string

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROGRESS_DIR = os.path.join(REPO_ROOT, "creation", "08-progress")
TASKS_FILE = os.path.join(REPO_ROOT, "creation", "07-tasks", "tasks.json")
MEMORY_FILE = os.path.join(REPO_ROOT, "creation", "05-memory", "memory.md")

# Ensure we can import local tools
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

# Try to import memory tools
try:
    from tools.add_memory_entry import append_entry as _append_entry_func
    from tools.add_memory_entry import write_memory_entry as _write_memory_entry_func
except Exception:
    _append_entry_func = None
    _write_memory_entry_func = None


def ensure_dir(path):
    """Ensure a directory exists."""
    os.makedirs(path, exist_ok=True)


def get_head_sha(branch="main"):
    """Get the HEAD SHA for the specified branch."""
    try:
        # Try to get SHA for the specified branch
        result = subprocess.run(
            ["git", "rev-parse", f"{branch}"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            return result.stdout.strip()
        
        # If branch doesn't exist, try refs/heads/<branch>
        result = subprocess.run(
            ["git", "rev-parse", f"refs/heads/{branch}"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            return result.stdout.strip()
        
        # If still no luck, use HEAD if we're on that branch or just use HEAD
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            return result.stdout.strip()
        
        return None
    except Exception:
        return None


def generate_session_id():
    """Generate a session ID in format ARCH_YYYYMMDD_HHMMSS_<short>."""
    now = datetime.datetime.now(datetime.timezone.utc)
    date_part = now.strftime("%Y%m%d")
    time_part = now.strftime("%H%M%S")
    # Generate a short random suffix (4 uppercase letters)
    random_suffix = ''.join(random.choices(string.ascii_uppercase, k=4))
    return f"ARCH_{date_part}_{time_part}_{random_suffix}"


def load_tasks():
    """Load tasks from tasks.json."""
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def load_latest_progress():
    """Load the latest progress from LATEST.json or most recent progress file."""
    latest_json = os.path.join(PROGRESS_DIR, "LATEST.json")
    
    # Try to load LATEST.json first
    if os.path.exists(latest_json):
        try:
            with open(latest_json, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    
    # Fallback: find most recent progress file
    try:
        if os.path.exists(PROGRESS_DIR):
            files = [f for f in os.listdir(PROGRESS_DIR) if f.endswith(".md") and f != "LATEST.json"]
            if files:
                files.sort(reverse=True)  # Most recent first
                latest_file = files[0]
                # Extract basic info from filename (YYYY-MM-DD.md)
                date = latest_file.replace(".md", "")
                return {
                    "date": date,
                    "file": f"creation/08-progress/{latest_file}",
                    "summary": "Previous session progress available",
                    "next_steps": []
                }
    except Exception:
        pass
    
    return None


def get_open_tasks(tasks, max_count=6):
    """Get a sample of open tasks."""
    open_tasks = [t for t in tasks if isinstance(t, dict) and t.get("status") != "complete"]
    return open_tasks[:max_count]


def generate_suggested_actions(open_tasks):
    """Generate suggested next actions from open tasks."""
    suggestions = []
    
    # Take up to 3 open tasks and convert them to action suggestions
    for i, task in enumerate(open_tasks[:3], 1):
        task_id = task.get("id", "")
        description = task.get("description", "Continue work")
        suggestions.append({
            "id": f"A{i}",
            "action": f"Work on {task_id}: {description}",
            "task_id": task_id
        })
    
    # Add a generic action if we have fewer than 3 tasks
    if len(suggestions) == 0:
        suggestions.append({
            "id": "A1",
            "action": "Review current state and plan next steps",
            "task_id": None
        })
    
    return suggestions


def append_session_boot_to_memory(session_id, head_sha):
    """Append a session_boot entry to memory.md."""
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00', 'Z')
    
    # Try import-based call first
    if _append_entry_func and _write_memory_entry_func:
        try:
            changes = [
                f"session_id: {session_id}",
                f"head_sha: {head_sha}"
            ]
            entry_text = _append_entry_func(
                event="session_boot",
                reasoning=f"Started new Architect session {session_id}",
                changes=changes
            )
            _write_memory_entry_func(entry_text)
            return True
        except Exception as e:
            print(f"Warning: import-based memory append failed: {e}", file=sys.stderr)
    
    # Manual fallback: append directly to memory.md
    try:
        entry = f"""
### [{timestamp}]
event: session_boot
reasoning: Started new Architect session {session_id}
changes:
  - session_id: {session_id}
  - head_sha: {head_sha}
"""
        with open(MEMORY_FILE, "a", encoding="utf-8") as f:
            f.write(entry)
        return True
    except Exception as e:
        print(f"Warning: manual memory append failed: {e}", file=sys.stderr)
        return False


def ensure_todays_progress_file():
    """Ensure today's progress file exists and return its path."""
    ensure_dir(PROGRESS_DIR)
    today = datetime.date.today().isoformat()
    filename = f"{today}.md"
    filepath = os.path.join(PROGRESS_DIR, filename)
    
    if not os.path.exists(filepath):
        # Create a minimal progress file for today
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# Progress Log — {today}\n\n")
            f.write("## Summary of Work Completed\n\n")
            f.write("- Session started\n\n")
    
    return filepath, filename


def update_latest_json(date, filename, sha, summary):
    """Update LATEST.json to point to today's progress file."""
    latest = {
        "date": date,
        "file": f"creation/08-progress/{filename}",
        "sha": sha or "",
        "summary": summary,
        "next_steps": [],
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00', 'Z'),
    }
    latest_path = os.path.join(PROGRESS_DIR, "LATEST.json")
    with open(latest_path, "w", encoding="utf-8") as f:
        json.dump(latest, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return latest_path


def generate_boot_report(session_id, branch, head_sha, dry_run=True):
    """Generate the JSON boot report."""
    # Load tasks
    tasks = load_tasks()
    open_tasks = get_open_tasks(tasks)
    
    # Load latest progress
    latest_progress = load_latest_progress()
    
    # Generate suggested actions
    suggested_actions = generate_suggested_actions(open_tasks)
    
    # Build the report
    report = {
        "session_id": session_id,
        "branch": branch,
        "head_sha": head_sha or "unknown",
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00', 'Z'),
        "dry_run": dry_run,
        "state": {
            "latest_progress": latest_progress,
            "memory_file": "creation/05-memory/memory.md",
            "tasks_file": "creation/07-tasks/tasks.json"
        },
        "tasks": {
            "total": len(tasks),
            "open": len([t for t in tasks if isinstance(t, dict) and t.get("status") != "complete"]),
            "complete": len([t for t in tasks if isinstance(t, dict) and t.get("status") == "complete"]),
            "open_sample": [
                {
                    "id": t.get("id"),
                    "description": t.get("description"),
                    "status": t.get("status")
                }
                for t in open_tasks
            ]
        },
        "suggested_next_actions": suggested_actions
    }
    
    return report


def main():
    parser = argparse.ArgumentParser(
        description="Generate CreateOS session boot report",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run (no memory changes, default)
  python tools/start_session.py --branch main --dry-run
  
  # Actual session start with memory entry
  python tools/start_session.py --branch main --commit
  
  # Just show help
  python tools/start_session.py --help
"""
    )
    parser.add_argument(
        "--branch",
        default="main",
        help="Git branch to use (default: main)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Dry run mode - do not write to memory or create progress files (default)"
    )
    parser.add_argument(
        "--commit",
        action="store_true",
        help="Commit mode - write session_boot to memory and create progress files"
    )
    
    args = parser.parse_args()
    
    # If --commit is specified, turn off dry-run
    dry_run = args.dry_run and not args.commit
    
    # Generate session ID
    session_id = generate_session_id()
    
    # Get HEAD SHA
    head_sha = get_head_sha(args.branch)
    if not head_sha:
        print(f"Error: Could not determine HEAD SHA for branch '{args.branch}'", file=sys.stderr)
        sys.exit(1)
    
    # If not dry-run, write memory and progress files
    if not dry_run:
        # Append session_boot to memory
        memory_success = append_session_boot_to_memory(session_id, head_sha)
        if not memory_success:
            print("Warning: Failed to write session_boot to memory.md", file=sys.stderr)
        
        # Ensure today's progress file exists
        progress_path, progress_filename = ensure_todays_progress_file()
        
        # Update LATEST.json
        today = datetime.date.today().isoformat()
        latest_path = update_latest_json(
            today,
            progress_filename,
            head_sha,
            f"Session {session_id} started"
        )
    
    # Generate and output the boot report
    report = generate_boot_report(session_id, args.branch, head_sha, dry_run)
    
    # Output JSON to stdout
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
