import argparse
import sys
from pathlib import Path

from src import storage
from src import tasks as task_ops

DEFAULT_PATH = Path("tasks.json")


def cmd_add(args: argparse.Namespace, path: Path) -> int:
    existing = storage.load_tasks(path)
    new_id = task_ops.next_id(existing)
    try:
        task = task_ops.create_task(id=new_id, title=args.title, priority=args.priority)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    existing.append(task)
    storage.save_tasks(existing, path)
    print(f"Added task {task['id']}: {task['title']} [{task['priority']}]")
    return 0


def cmd_list(args: argparse.Namespace, path: Path) -> int:
    existing = storage.load_tasks(path)
    status_filter = getattr(args, "status", None)
    priority_filter = getattr(args, "priority", None)
    result = task_ops.list_tasks(existing, status=status_filter)
    if priority_filter:
        result = task_ops.filter_by_priority(result, priority_filter)
    if not result:
        print("No tasks found.")
        return 0
    for t in result:
        priority = t.get("priority", "medium")
        print(f"[{t['id']}] {t['title']} ({t['status']}) [{priority}]")
    return 0


def cmd_done(args: argparse.Namespace, path: Path) -> int:
    existing = storage.load_tasks(path)
    try:
        updated = task_ops.mark_done(existing, args.id)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    storage.save_tasks(updated, path)
    print(f"Task {args.id} marked as done.")
    return 0


def cmd_delete(args: argparse.Namespace, path: Path) -> int:
    existing = storage.load_tasks(path)
    try:
        updated = task_ops.delete_task(existing, args.id)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    storage.save_tasks(updated, path)
    print(f"Task {args.id} deleted.")
    return 0


def cmd_show(args: argparse.Namespace, path: Path) -> int:
    existing = storage.load_tasks(path)
    for task in existing:
        if task["id"] == args.id:
            print(f"ID:       {task['id']}")
            print(f"Title:    {task['title']}")
            print(f"Status:   {task['status']}")
            print(f"Priority: {task.get('priority', 'medium')}")
            print(f"Created:  {task['created_at']}")
            return 0
    print(f"Error: Task {args.id} not found.", file=sys.stderr)
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="src", description="CLI task tracker")
    sub = parser.add_subparsers(dest="command")
    sub.required = True

    add_p = sub.add_parser("add", help="Add a new task")
    add_p.add_argument("title", help="Task title")
    add_p.add_argument(
        "--priority", choices=["low", "medium", "high"], default="medium",
        help="Task priority (default: medium)",
    )

    list_p = sub.add_parser("list", help="List tasks")
    list_p.add_argument("--status", choices=["pending", "done"], default=None)
    list_p.add_argument("--priority", choices=["low", "medium", "high"], default=None)

    done_p = sub.add_parser("done", help="Mark a task as done")
    done_p.add_argument("id", type=int)

    del_p = sub.add_parser("delete", help="Delete a task")
    del_p.add_argument("id", type=int)

    show_p = sub.add_parser("show", help="Show full details of a task")
    show_p.add_argument("id", type=int)

    return parser


def main(argv: list = None, path: Path = DEFAULT_PATH) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    handlers = {
        "add": cmd_add,
        "list": cmd_list,
        "done": cmd_done,
        "delete": cmd_delete,
        "show": cmd_show,
    }
    code = handlers[args.command](args, path)
    sys.exit(code)
