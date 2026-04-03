import argparse
import sys
from pathlib import Path

from src import storage
from src import tasks as task_ops

DEFAULT_PATH = Path("tasks.json")


def cmd_add(args: argparse.Namespace, path: Path) -> int:
    existing = storage.load_tasks(path)
    new_id = task_ops.next_id(existing)
    task = task_ops.create_task(id=new_id, title=args.title)
    existing.append(task)
    storage.save_tasks(existing, path)
    print(f"Added task {task['id']}: {task['title']}")
    return 0


def cmd_list(args: argparse.Namespace, path: Path) -> int:
    existing = storage.load_tasks(path)
    status_filter = getattr(args, "status", None)
    result = task_ops.list_tasks(existing, status=status_filter)
    if not result:
        print("No tasks found.")
        return 0
    for t in result:
        print(f"[{t['id']}] {t['title']} ({t['status']})")
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="src", description="CLI task tracker")
    sub = parser.add_subparsers(dest="command")
    sub.required = True

    add_p = sub.add_parser("add", help="Add a new task")
    add_p.add_argument("title", help="Task title")

    list_p = sub.add_parser("list", help="List tasks")
    list_p.add_argument("--status", choices=["pending", "done"], default=None)

    done_p = sub.add_parser("done", help="Mark a task as done")
    done_p.add_argument("id", type=int)

    del_p = sub.add_parser("delete", help="Delete a task")
    del_p.add_argument("id", type=int)

    return parser


def main(argv: list = None, path: Path = DEFAULT_PATH) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    handlers = {
        "add": cmd_add,
        "list": cmd_list,
        "done": cmd_done,
        "delete": cmd_delete,
    }
    code = handlers[args.command](args, path)
    sys.exit(code)
