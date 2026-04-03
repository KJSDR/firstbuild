import json
from pathlib import Path
from typing import Any, Dict, List

DEFAULT_PATH = Path("tasks.json")


def load_tasks(path: Path = DEFAULT_PATH) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    with open(path) as f:
        return json.load(f)


def save_tasks(tasks: List[Dict[str, Any]], path: Path = DEFAULT_PATH) -> None:
    with open(path, "w") as f:
        json.dump(tasks, f, indent=2)
