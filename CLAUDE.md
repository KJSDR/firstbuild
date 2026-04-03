# CLAUDE.md — Python CLI Task Tracker

## Project Overview

A command-line task tracker that stores tasks as JSON. Users can add, list, complete, and delete tasks via CLI commands.

## Tech Stack

- **Language**: Python 3.11+
- **CLI parsing**: `argparse` (stdlib)
- **Storage**: JSON file (`tasks.json`)
- **Testing**: `pytest`
- **No third-party dependencies** beyond pytest

## Project Structure

```
firstbuild/
├── README.md
├── CLAUDE.md
├── spec.md
├── src/
│   ├── __init__.py
│   ├── cli.py          # argparse entry point, subcommands
│   ├── storage.py      # Load/save tasks.json
│   └── tasks.py        # Task data model and business logic
└── tests/
    ├── __init__.py
    ├── test_cli.py
    ├── test_storage.py
    └── test_tasks.py
```

- `tasks.json` is generated at runtime in the working directory (git-ignored)
- Project metadata and pytest config live in `pyproject.toml` at the root

## Conventions

### Code style
- Follow PEP 8. Use 4-space indentation.
- Use type hints on all function signatures.
- Keep functions small and single-purpose.
- No global state outside of `storage.py`.

### CLI subcommands
Implemented as argparse subparsers in `cli.py`:

| Command | Description |
|---------|-------------|
| `add <title>` | Add a new task |
| `list` | List all tasks (pending by default) |
| `done <id>` | Mark a task as complete |
| `delete <id>` | Remove a task permanently |

### Task schema (JSON)
```json
{
  "id": 1,
  "title": "Buy groceries",
  "status": "pending",
  "created_at": "2026-04-03T14:00:00"
}
```
- `status` is either `"pending"` or `"done"`.
- IDs are integers, auto-incremented from the stored list.

### Storage
- `storage.py` is the only module that reads/writes `tasks.json`.
- Default path is `tasks.json` in the working directory; tests override it via a fixture.
- Always write JSON with `indent=2` for readability.

## Testing Expectations

- **All business logic must be tested.** Functions in `tasks.py` and `storage.py` need full coverage.
- **CLI tests** use `argparse` parsing directly or `subprocess` — do not mock `sys.argv` inline.
- **Never use the real `tasks.json`** in tests. Use `tmp_path` (pytest fixture) to create a temp file and pass it to storage functions.
- **No mocking the filesystem** — tests hit real temp files. This avoids mock/prod divergence.
- Run tests with:
  ```bash
  pytest
  ```
- All tests must pass before committing.

## Running the CLI

```bash
python -m src add "Write CLAUDE.md"
python -m src list
python -m src done 1
python -m src delete 1
```

## What to Avoid

- Do not add a database or ORM — JSON storage is intentional.
- Do not introduce external dependencies without discussion.
- Do not write tests that mock the storage layer; use real temp files.
- Do not put business logic in `cli.py` — it should only parse and dispatch.
