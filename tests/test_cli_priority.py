"""CLI tests for priority flag and show subcommand (Level 2 — multi-file).

Design decisions documented here:
- `add --priority` defaults to 'medium'; argparse choices enforce valid values.
- `list --priority` and `--status` are independent filters applied together (AND).
- Priority is shown inline in list output: [id] title (status) [priority].
- `show <id>` is a dedicated subcommand printing all task fields.

Covers AC-2 extension (priority filtering) and new show functionality.
Written before implementation — fails until cli.py is updated.
"""

import json
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def run(args: list, cwd: Path):
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
# add --priority
# ---------------------------------------------------------------------------

class TestAddPriority:
    def test_add_stores_high_priority(self, tmp_path):
        run(["add", "Urgent", "--priority", "high"], tmp_path)
        data = json.loads((tmp_path / "tasks.json").read_text())
        assert data[0]["priority"] == "high"

    def test_add_stores_low_priority(self, tmp_path):
        run(["add", "Later", "--priority", "low"], tmp_path)
        data = json.loads((tmp_path / "tasks.json").read_text())
        assert data[0]["priority"] == "low"

    def test_add_default_priority_is_medium(self, tmp_path):
        run(["add", "Normal"], tmp_path)
        data = json.loads((tmp_path / "tasks.json").read_text())
        assert data[0]["priority"] == "medium"

    def test_add_invalid_priority_nonzero_exit(self, tmp_path):
        result = run(["add", "Bad", "--priority", "urgent"], tmp_path)
        assert result.returncode != 0

    def test_add_invalid_priority_no_json_created(self, tmp_path):
        run(["add", "Bad", "--priority", "urgent"], tmp_path)
        assert not (tmp_path / "tasks.json").exists()


# ---------------------------------------------------------------------------
# list --priority filter
# ---------------------------------------------------------------------------

class TestListPriority:
    def test_list_priority_high_shows_only_high(self, tmp_path):
        run(["add", "High task", "--priority", "high"], tmp_path)
        run(["add", "Low task", "--priority", "low"], tmp_path)
        result = run(["list", "--priority", "high"], tmp_path)
        assert "High task" in result.stdout
        assert "Low task" not in result.stdout

    def test_list_shows_priority_in_output(self, tmp_path):
        run(["add", "Task", "--priority", "high"], tmp_path)
        result = run(["list"], tmp_path)
        assert "high" in result.stdout

    def test_list_priority_and_status_combined(self, tmp_path):
        run(["add", "High pending", "--priority", "high"], tmp_path)
        run(["add", "High done", "--priority", "high"], tmp_path)
        run(["done", "2"], tmp_path)
        result = run(["list", "--priority", "high", "--status", "pending"], tmp_path)
        assert "High pending" in result.stdout
        assert "High done" not in result.stdout

    def test_list_invalid_priority_nonzero_exit(self, tmp_path):
        result = run(["list", "--priority", "urgent"], tmp_path)
        assert result.returncode != 0


# ---------------------------------------------------------------------------
# show subcommand
# ---------------------------------------------------------------------------

class TestShow:
    def test_show_exits_zero(self, tmp_path):
        run(["add", "Buy milk"], tmp_path)
        result = run(["show", "1"], tmp_path)
        assert result.returncode == 0

    def test_show_prints_title(self, tmp_path):
        run(["add", "Buy milk"], tmp_path)
        result = run(["show", "1"], tmp_path)
        assert "Buy milk" in result.stdout

    def test_show_prints_status(self, tmp_path):
        run(["add", "Buy milk"], tmp_path)
        result = run(["show", "1"], tmp_path)
        assert "pending" in result.stdout

    def test_show_prints_priority(self, tmp_path):
        run(["add", "Buy milk", "--priority", "high"], tmp_path)
        result = run(["show", "1"], tmp_path)
        assert "high" in result.stdout

    def test_show_prints_id(self, tmp_path):
        run(["add", "Buy milk"], tmp_path)
        result = run(["show", "1"], tmp_path)
        assert "1" in result.stdout

    def test_show_prints_created_at(self, tmp_path):
        run(["add", "Buy milk"], tmp_path)
        result = run(["show", "1"], tmp_path)
        assert "created" in result.stdout.lower() or "202" in result.stdout

    def test_show_missing_id_nonzero_exit(self, tmp_path):
        result = run(["show", "99"], tmp_path)
        assert result.returncode != 0

    def test_show_missing_id_prints_error(self, tmp_path):
        result = run(["show", "99"], tmp_path)
        assert "99" in result.stderr
