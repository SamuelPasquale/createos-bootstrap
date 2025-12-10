#!/usr/bin/env python3
"""
Tool: tasks.py
Purpose: Manage the task graph in creation/07-tasks/tasks.json
Creation: C01 – CreateOS Bootstrap
"""

import os
import json
import argparse
from typing import List, Dict

TASKS_FILE_PATH = "creation/07-tasks/tasks.json"


def load_tasks() -> List[Dict]:
    if not os.path.exists(TASKS_FILE_PATH):
        raise FileNotFoundError(f"Tasks file not found at: {TASKS_FILE_PATH}")
    with open(TASKS_FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tasks(tasks: List[Dict]) -> None:
    with open(TASKS_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)


def list_tasks(tasks: List[Dict]) -> None:
    for t in tasks:
        deps = ", ".join(t.get("dependencies", []))
        print(f"{t['id']} [{t['status']}] - {t['description']} (deps: {deps})")


def add_task(tasks: List[Dict], task_id: str, description: str, dependencies: List[str]) -> List[Dict]:
    existing_ids = {t["id"] for t in tasks}
    if task_id in existing_ids:
        raise ValueError(f"Task with id {task_id} already exists.")

    new_task = {
        "id": task_id,
        "description": description,
        "status": "pending",
        "dependencies": dependencies,
    }
    tasks.append(new_task)
    return tasks


def update_status(tasks: List[Dict], task_id: str, status: str) -> List[Dict]:
    valid_statuses = {"pending", "in_progress", "complete"}
    if status not in valid_statuses:
        raise ValueError(f"Invalid status '{status}'. Must be one of {valid_statuses}.")

    for t in tasks:
        if t["id"] == task_id:
            t["status"] = status
            break
    else:
        raise ValueError(f"Task with id {task_id} not found.")
    return tasks


def main():
    parser = argparse.ArgumentParser(description="Manage the Creation task graph.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # list
    subparsers.add_parser("list", help="List all tasks.")

    # add
    add_parser = subparsers.add_parser("add", help="Add a new task.")
    add_parser.add_argument("--id", required=True, help="Task ID (e.g., T004).")
    add_parser.add_argument("--description", required=True, help="Task description.")
    add_parser.add_argument(
        "--dependencies",
        nargs="*",
        default=[],
        help="List of dependency task IDs.",
    )

    # update-status
    update_parser = subparsers.add_parser("update-status", help="Update the status of a task.")
    update_parser.add_argument("--id", required=True, help="Task ID.")
    update_parser.add_argument(
        "--status",
        required=True,
        choices=["pending", "in_progress", "complete"],
        help="New status for the task.",
    )

    args = parser.parse_args()
    tasks = load_tasks()

    if args.command == "list":
        list_tasks(tasks)
    elif args.command == "add":
        tasks = add_task(tasks, args.id, args.description, args.dependencies)
        save_tasks(tasks)
        print(f"Task {args.id} added.")
    elif args.command == "update-status":
        tasks = update_status(tasks, args.id, args.status)
        save_tasks(tasks)
        print(f"Task {args.id} status updated to {args.status}.")


if __name__ == "__main__":
    main()
