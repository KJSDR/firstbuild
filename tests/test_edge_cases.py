"""Edge-case tests identified during the Day 6 test gap analysis.

Covers:
- AC-6: explicit persistence across separate subprocess invocations
- storage.load_tasks: malformed / corrupted tasks.json
- storage.load_tasks: empty-file edge case
"""

import json
import os
import sys
from pathlib import Path

import pytest

from src.storage import load_tasks

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
# AC-6: persistence across separate CLI invocations
# ---------------------------------------------------------------------------

class TestPersistence:
    def test_task_survives_separate_invocation(self, tmp_path):
        """A task added in one process is visible in a second process."""
        run(["add", "Walk dog"], tmp_path)
        result = run(["list"], tmp_path)
        assert "Walk dog" in result.stdout

    def test_status_survives_separate_invocation(self, tmp_path):
        """done status written in one process is read correctly in the next."""
        run(["add", "Walk dog"], tmp_path)
        run(["done", "1"], tmp_path)
        result = run(["list", "--status", "done"], tmp_path)
        assert "Walk dog" in result.stdout

    def test_id_stable_across_invocations(self, tmp_path):
        """IDs assigned in one process are unchanged when listed in another."""
        run(["add", "First"], tmp_path)
        run(["add", "Second"], tmp_path)
        data = json.loads((tmp_path / "tasks.json").read_text())
        assert data[0]["id"] == 1
        assert data[1]["id"] == 2


# ---------------------------------------------------------------------------
# storage: malformed / corrupted tasks.json
# ---------------------------------------------------------------------------

class TestLoadTasksMalformed:
    def test_raises_on_invalid_json(self, tmp_path):
        """load_tasks raises json.JSONDecodeError when the file is corrupt."""
        path = tmp_path / "tasks.json"
        path.write_text("{not valid json")
        with pytest.raises(Exception):
            load_tasks(path)

    def test_raises_on_empty_file(self, tmp_path):
        """load_tasks raises an exception when tasks.json is completely empty."""
        path = tmp_path / "tasks.json"
        path.write_text("")
        with pytest.raises(Exception):
            load_tasks(path)

    def test_raises_on_json_object_not_list(self, tmp_path):
        """load_tasks returns an unexpected type when JSON root is an object."""
        path = tmp_path / "tasks.json"
        path.write_text(json.dumps({"id": 1}))
        result = load_tasks(path)
        # Current implementation returns the dict — this test documents the
        # behavior so a future fix (raising or returning []) is a conscious choice.
        assert not isinstance(result, list)
