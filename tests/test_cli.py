"""End-to-end CLI tests using subprocess (src/cli.py + src/__main__.py).

Covers AC-1, AC-2, AC-3, AC-4, AC-5, AC-7.
Uses tmp_path as cwd so the real tasks.json is never touched.
Written before implementation — fails until cli.py and __main__.py exist.
"""

import json
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def run(args: list, cwd: Path):
    """Run `python -m src <args>` with PYTHONPATH set to the project root."""
    import subprocess

    env = {**os.environ, "PYTHONPATH": str(PROJECT_ROOT)}
    return subprocess.run(
        [sys.executable, "-m", "src"] + args,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        env=env,
    )


# ---------------------------------------------------------------------------
# AC-1: add creates a persistent record
# ---------------------------------------------------------------------------

class TestAdd:
    def test_exits_zero(self, tmp_path):
        result = run(["add", "Buy milk"], tmp_path)
        assert result.returncode == 0

    def test_prints_task_id(self, tmp_path):
        result = run(["add", "Buy milk"], tmp_path)
        assert "1" in result.stdout

    def test_creates_tasks_json(self, tmp_path):
        run(["add", "Buy milk"], tmp_path)
        assert (tmp_path / "tasks.json").exists()

    def test_tasks_json_contains_task(self, tmp_path):
        run(["add", "Buy milk"], tmp_path)
        data = json.loads((tmp_path / "tasks.json").read_text())
        assert len(data) == 1
        assert data[0]["title"] == "Buy milk"
        assert data[0]["status"] == "pending"

    def test_second_add_gets_incremented_id(self, tmp_path):
        run(["add", "First"], tmp_path)
        run(["add", "Second"], tmp_path)
        data = json.loads((tmp_path / "tasks.json").read_text())
        assert data[0]["id"] == 1
        assert data[1]["id"] == 2


# ---------------------------------------------------------------------------
# AC-2: list filters by status
# ---------------------------------------------------------------------------

class TestList:
    def test_list_shows_all_by_default(self, tmp_path):
        run(["add", "Task A"], tmp_path)
        run(["add", "Task B"], tmp_path)
        result = run(["list"], tmp_path)
        assert "Task A" in result.stdout
        assert "Task B" in result.stdout

    def test_list_pending_excludes_done(self, tmp_path):
        run(["add", "Task A"], tmp_path)
        run(["add", "Task B"], tmp_path)
        run(["done", "1"], tmp_path)
        result = run(["list", "--status", "pending"], tmp_path)
        assert "Task A" not in result.stdout
        assert "Task B" in result.stdout

    def test_list_done_shows_only_done(self, tmp_path):
        run(["add", "Task A"], tmp_path)
        run(["add", "Task B"], tmp_path)
        run(["done", "1"], tmp_path)
        result = run(["list", "--status", "done"], tmp_path)
        assert "Task A" in result.stdout
        assert "Task B" not in result.stdout

    def test_list_exits_zero(self, tmp_path):
        result = run(["list"], tmp_path)
        assert result.returncode == 0


# ---------------------------------------------------------------------------
# AC-3: done marks a task as done
# ---------------------------------------------------------------------------

class TestDone:
    def test_exits_zero(self, tmp_path):
        run(["add", "Buy milk"], tmp_path)
        result = run(["done", "1"], tmp_path)
        assert result.returncode == 0

    def test_updates_status_in_json(self, tmp_path):
        run(["add", "Buy milk"], tmp_path)
        run(["done", "1"], tmp_path)
        data = json.loads((tmp_path / "tasks.json").read_text())
        assert data[0]["status"] == "done"

    def test_preserves_title_in_json(self, tmp_path):
        run(["add", "Buy milk"], tmp_path)
        run(["done", "1"], tmp_path)
        data = json.loads((tmp_path / "tasks.json").read_text())
        assert data[0]["title"] == "Buy milk"


# ---------------------------------------------------------------------------
# AC-4: delete removes a task permanently
# ---------------------------------------------------------------------------

class TestDelete:
    def test_exits_zero(self, tmp_path):
        run(["add", "Buy milk"], tmp_path)
        result = run(["delete", "1"], tmp_path)
        assert result.returncode == 0

    def test_task_absent_from_json(self, tmp_path):
        run(["add", "Task A"], tmp_path)
        run(["add", "Task B"], tmp_path)
        run(["delete", "1"], tmp_path)
        data = json.loads((tmp_path / "tasks.json").read_text())
        assert all(t["id"] != 1 for t in data)
        assert len(data) == 1

    def test_remaining_task_still_present(self, tmp_path):
        run(["add", "Task A"], tmp_path)
        run(["add", "Task B"], tmp_path)
        run(["delete", "1"], tmp_path)
        data = json.loads((tmp_path / "tasks.json").read_text())
        assert data[0]["title"] == "Task B"


# ---------------------------------------------------------------------------
# AC-5: invalid ID fails gracefully
# ---------------------------------------------------------------------------

class TestInvalidId:
    def test_done_missing_id_nonzero_exit(self, tmp_path):
        run(["add", "Buy milk"], tmp_path)
        result = run(["done", "99"], tmp_path)
        assert result.returncode != 0

    def test_done_missing_id_prints_error(self, tmp_path):
        run(["add", "Buy milk"], tmp_path)
        result = run(["done", "99"], tmp_path)
        assert "99" in result.stderr

    def test_done_does_not_modify_json(self, tmp_path):
        run(["add", "Buy milk"], tmp_path)
        before = (tmp_path / "tasks.json").read_text()
        run(["done", "99"], tmp_path)
        after = (tmp_path / "tasks.json").read_text()
        assert before == after

    def test_delete_missing_id_nonzero_exit(self, tmp_path):
        run(["add", "Buy milk"], tmp_path)
        result = run(["delete", "99"], tmp_path)
        assert result.returncode != 0

    def test_delete_missing_id_prints_error(self, tmp_path):
        run(["add", "Buy milk"], tmp_path)
        result = run(["delete", "99"], tmp_path)
        assert "99" in result.stderr


# ---------------------------------------------------------------------------
# AC-7: missing title is rejected
# ---------------------------------------------------------------------------

class TestMissingTitle:
    def test_add_no_title_nonzero_exit(self, tmp_path):
        result = run(["add"], tmp_path)
        assert result.returncode != 0

    def test_add_no_title_does_not_create_json(self, tmp_path):
        run(["add"], tmp_path)
        assert not (tmp_path / "tasks.json").exists()
