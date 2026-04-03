# spec.md — Python CLI Task Tracker

## Purpose

This document defines the functional requirements and quality gates for the CLI task tracker. A build is considered passing only when all quality gates below are satisfied.

---

## Functional Requirements

1. Users can add a task with a title.
2. Users can list all tasks, filtered by status (default: all).
3. Users can mark a task as done by ID.
4. Users can delete a task by ID.
5. Tasks persist across CLI invocations via a JSON file.
6. Each task has a unique integer ID, a title, a status (`pending` or `done`), and a creation timestamp.

---

## Acceptance Criteria

### AC-1 — Adding a task creates a persistent record

**Given** the task store is empty
**When** the user runs `python -m src add "Buy milk"`
**Then** the command exits with code `0`, prints a confirmation containing the new task's ID, and `tasks.json` contains exactly one entry with `"title": "Buy milk"` and `"status": "pending"`

---

### AC-2 — Listing tasks shows only matching status

**Given** two tasks exist: task 1 is `pending`, task 2 is `done`
**When** the user runs `python -m src list --status pending`
**Then** the output contains task 1 and does not contain task 2

---

### AC-3 — Marking a task done changes its status

**Given** a task with ID `1` exists and has status `pending`
**When** the user runs `python -m src done 1`
**Then** the command exits with code `0`, and `tasks.json` shows task 1 with `"status": "done"`; the task's `title` and `created_at` are unchanged

---

### AC-4 — Deleting a task removes it permanently

**Given** two tasks exist with IDs `1` and `2`
**When** the user runs `python -m src delete 1`
**Then** the command exits with code `0`, and subsequent `python -m src list` output contains task 2 but not task 1; `tasks.json` has exactly one entry

---

### AC-5 — Operating on a non-existent ID fails gracefully

**Given** the task store contains only task ID `1`
**When** the user runs `python -m src done 99` or `python -m src delete 99`
**Then** the command exits with a non-zero code and prints a human-readable error message (e.g. `"Task 99 not found"`); `tasks.json` is not modified

---

### AC-6 — Tasks persist across separate CLI invocations

**Given** the user runs `python -m src add "Walk dog"` and the process exits
**When** the user runs `python -m src list` in a new invocation
**Then** the output contains the previously added task with its correct ID, title, and status

---

### AC-7 — Adding a task with no title is rejected

**Given** the CLI is invoked
**When** the user runs `python -m src add` with no title argument
**Then** the command exits with a non-zero code and prints a usage or error message; `tasks.json` is not created or modified

---

## Quality Gates

### Gate 1 — Test Suite Passes

**Invoke:**
```bash
pytest tests/
```

**Success criteria:**
- Exit code is `0`.
- Output shows `0 failed`, `0 errors`.
- Every function in `src/tasks.py` and `src/storage.py` has at least one direct test in `tests/`.

---

### Gate 2 — Test Coverage ≥ 80%

**Invoke:**
```bash
pytest tests/ --cov=src --cov-report=term-missing --cov-fail-under=80
```

**Success criteria:**
- Exit code is `0`.
- The `TOTAL` line in the coverage report shows `≥ 80%`.
- No module in `src/` falls below `70%` individually.

---

### Gate 3 — Type Checking Passes

**Invoke:**
```bash
mypy src/
```

**Success criteria:**
- Exit code is `0`.
- Output reads `Success: no issues found`.
- All functions in `src/` have type-annotated parameters and return types.

---

### Gate 4 — Lint Passes with No Errors

**Invoke:**
```bash
ruff check src/ tests/
```

**Success criteria:**
- Exit code is `0`.
- No errors or warnings are printed.
- Code conforms to PEP 8 line length (max 88 characters).

---

### Gate 5 — CLI Smoke Test

**Invoke** (run sequentially in a clean temp directory):
```bash
cd $(mktemp -d)
python -m src add "Buy milk"
python -m src add "Walk dog"
python -m src list
python -m src done 1
python -m src list --status done
python -m src delete 2
python -m src list
```

**Success criteria:**
- Each command exits with code `0`.
- `list` after two adds shows two tasks with status `pending`.
- `done 1` prints a confirmation and changes task 1 status to `done`.
- `list --status done` shows exactly task 1 and nothing else.
- `delete 2` removes task 2; final `list` shows only task 1.
- `tasks.json` exists in the temp directory and is valid JSON after all commands.
