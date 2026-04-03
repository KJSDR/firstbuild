from datetime import datetime
from typing import Any, Dict, List, Optional

VALID_PRIORITIES = {"low", "medium", "high"}
_PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def create_task(id: int, title: str, priority: str = "medium") -> Dict[str, Any]:
    if not title or not title.strip():
        raise ValueError("Title cannot be empty or whitespace.")
    if priority not in VALID_PRIORITIES:
        raise ValueError(f"Invalid priority '{priority}'. Must be one of: low, medium, high.")
    return {
        "id": id,
        "title": title,
        "status": "pending",
        "priority": priority,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }


def sort_by_priority(tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return sorted(tasks, key=lambda t: _PRIORITY_ORDER.get(t.get("priority", "medium"), 1))


def filter_by_priority(tasks: List[Dict[str, Any]], priority: str) -> List[Dict[str, Any]]:
    return [t for t in tasks if t.get("priority", "medium") == priority]


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


def delete_task(tasks: List[Dict[str, Any]], task_id: int) -> List[Dict[str, Any]]:
    for task in tasks:
        if task["id"] == task_id:
            return [t for t in tasks if t["id"] != task_id]
    raise ValueError(f"Task {task_id} not found.")


def list_tasks(
    tasks: List[Dict[str, Any]], status: Optional[str] = None
) -> List[Dict[str, Any]]:
    if status is None:
        return tasks
    return [t for t in tasks if t["status"] == status]
