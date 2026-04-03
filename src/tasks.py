from datetime import datetime
from typing import Any, Dict, List


def create_task(id: int, title: str) -> Dict[str, Any]:
    if not title or not title.strip():
        raise ValueError("Title cannot be empty or whitespace.")
    return {
        "id": id,
        "title": title,
        "status": "pending",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
