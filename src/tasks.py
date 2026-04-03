from datetime import datetime
from typing import Any, Dict, List, Optional


def create_task(id: int, title: str) -> Dict[str, Any]:
    if not title or not title.strip():
        raise ValueError("Title cannot be empty or whitespace.")
    return {
        "id": id,
        "title": title,
        "status": "pending",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }


def next_id(tasks: List[Dict[str, Any]]) -> int:
    if not tasks:
        return 1
    return max(t["id"] for t in tasks) + 1


def mark_done(tasks: List[Dict[str, Any]], task_id: int) -> List[Dict[str, Any]]:
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "done"
            return tasks
    raise ValueError(f"Task {task_id} not found.")
