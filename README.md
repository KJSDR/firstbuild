# CLI Task Tracker

A command-line task tracker built in Python. Tasks are stored as JSON and managed through subcommands. Built as a learning project to practice test-driven development workflows.

---

## Usage

```bash
python -m src add "Buy milk"
python -m src add "Urgent fix" --priority high
python -m src list
python -m src list --status pending
python -m src list --priority high
python -m src list --status pending --priority high
python -m src show 1
python -m src done 1
python -m src delete 2
```

## Commands

| Command | Description |
|---------|-------------|
| `add <title> [--priority low\|medium\|high]` | Add a new task |
| `list [--status pending\|done] [--priority low\|medium\|high]` | List tasks with optional filters |
| `show <id>` | Show full details for a single task |
| `done <id>` | Mark a task as done |
| `delete <id>` | Remove a task permanently |

## Task schema

Each task in `tasks.json` looks like:

```json
{
  "id": 1,
  "title": "Buy milk",
  "status": "pending",
  "priority": "medium",
  "created_at": "2026-04-03T14:00:00"
}
```

## Running tests

```bash
python3 -m pytest tests/
```

---

## How I built this — v1.1 and v1.2 Workflow Documentation

### Overview

This project was built in two lab versions (v1.1 and v1.2) following a strict **test-driven development (TDD)** workflow. Every feature was developed in a red/green/refactor cycle with tests committed to git _before_ any implementation code.

---

### v1.1 — Test-First Development

The core of v1.1 was practising the TDD loop across four features. For each one, the cycle was:

1. **Write failing tests** → commit (red)
2. **Write the minimum implementation** to make them pass → commit (green)
3. **Refactor** if needed while keeping tests green

#### Feature 1 — `create_task` + storage

The first set of tests (`test_tasks.py`, `test_storage.py`) was written before any `src/` code existed. Both files failed immediately with `ModuleNotFoundError` — which is exactly the right starting state for TDD. Once I was sure they failed for the right reason (missing implementation, not a broken test), I committed them and then implemented `tasks.py` and `storage.py`.

One thing I corrected mid-process: my first implementation commit accidentally included `mark_done`, `delete_task`, and `list_tasks` before their tests were written. I caught this, used `git reset --soft` to undo the commit, trimmed the functions back out, and recommitted only what was tested. This kept the commit history honest.

#### Feature 2 — `mark_done` + `next_id`

Same loop. Tests written first in `test_mark_done.py`, committed while red, then implemented. The tests here were more specific — they checked that `mark_done` does not touch other tasks, and that on a missing ID the list is not mutated. Writing those assertions first forced the implementation to be precise.

#### Feature 3 — `delete_task` + `list_tasks`

Notable design constraint from the tests: `delete_task` must return a new list without mutating the original. Writing the test `test_does_not_mutate_original_list` first forced this decision — if I had written the implementation first I might have mutated in place.

#### Feature 4 — CLI

CLI tests use `subprocess` and `tmp_path` as the working directory (so `tasks.json` is always written to a temp folder, never the real project directory). This matched the guidance in `CLAUDE.md` to avoid mocking the filesystem. All 22 CLI tests covered the acceptance criteria from `spec.md`.

---

### v1.2 — Complexity & Polish

v1.2 introduced two features at different complexity levels to practice different workflow approaches.

#### Level 1 — Single-file area: `priority` field (`tasks.py` only)

**What changed:** `create_task` gained an optional `priority` parameter (`low` / `medium` / `high`, default `medium`). Two new functions were added: `sort_by_priority` and `filter_by_priority`.

**Workflow used:** Because this was a single-file change, I kept everything local to `tasks.py` and `test_priority.py`. I wrote all tests first, ran them to confirm the import errors, committed, then implemented. No design coordination across files was needed — the shape of the API was obvious from the tests themselves.

**Key decision:** `sort_by_priority` returns a new sorted list rather than sorting in place. Writing `test_does_not_mutate_original_list` first locked this in before I wrote a single line of implementation.

#### Level 2 — Multi-file, design decisions: priority CLI + `show` subcommand (`cli.py` + `tasks.py`)

**What changed:** Priority was wired through the CLI (`add --priority`, `list --priority`), and a new `show <id>` subcommand was added to display all task fields.

**Workflow used:** Multi-file tasks required an upfront design step before writing tests. I documented these decisions in the test module's docstring:

1. **`show` as a dedicated subcommand** — not overloading `list <id>`. Dedicated subcommands are easier to test and keep the parser simple.
2. **`--status` and `--priority` are AND-filters** — both apply together. The logic stays in the CLI layer, not inside `list_tasks`, to keep `tasks.py` functions single-purpose.
3. **Invalid `--priority` rejected by argparse `choices=`** — no extra validation in the CLI handler needed. This avoids duplicating what argparse already does.
4. **Priority shown inline in list output** — `[1] Buy milk (pending) [high]` — compact and machine-parseable.

Only after writing these decisions down did I write the tests. This top-down approach (decisions → tests → implementation) worked better for multi-file work than jumping straight into tests, because the tests needed to agree on the interface before any file was touched.

---

### What the commit history shows

The git log reflects the discipline of the workflow. For every feature:

```
[red]   add failing tests for <feature>
[green] implement <feature>
```

This pattern appears four times in v1.1 and twice in v1.2, giving a full audit trail that tests always preceded implementation.
