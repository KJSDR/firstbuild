"""Tests for JSON storage layer (src/storage.py).

Covers persistence behaviour from AC-1 and AC-6.
Uses pytest's tmp_path fixture so the real tasks.json is never touched.
These tests are written before any implementation exists and should fail
with ImportError until src/storage.py is written.
"""

import json
import pytest
from src.storage import load_tasks, save_tasks


class TestLoadTasks:
    def test_returns_empty_list_when_file_missing(self, tmp_path):
        """Loading from a non-existent path returns an empty list."""
        path = tmp_path / "tasks.json"
        result = load_tasks(path)
        assert result == []

    def test_returns_tasks_from_existing_file(self, tmp_path):
        """Tasks written to disk are returned correctly."""
        path = tmp_path / "tasks.json"
        data = [{"id": 1, "title": "Buy milk", "status": "pending", "created_at": "2026-04-03T14:00:00"}]
        path.write_text(json.dumps(data))
        result = load_tasks(path)
        assert result == data

    def test_returns_list_type(self, tmp_path):
        """load_tasks always returns a list, never None."""
        path = tmp_path / "tasks.json"
        result = load_tasks(path)
        assert isinstance(result, list)


class TestSaveTasks:
    def test_creates_file(self, tmp_path):
        """save_tasks creates the JSON file if it does not exist."""
        path = tmp_path / "tasks.json"
        save_tasks([], path)
        assert path.exists()

    def test_written_file_is_valid_json(self, tmp_path):
        """The file written by save_tasks is valid JSON."""
        path = tmp_path / "tasks.json"
        save_tasks([], path)
        content = json.loads(path.read_text())
        assert isinstance(content, list)

    def test_round_trip(self, tmp_path):
        """Tasks saved then loaded are identical to the originals."""
        path = tmp_path / "tasks.json"
        tasks = [{"id": 1, "title": "Walk dog", "status": "pending", "created_at": "2026-04-03T09:00:00"}]
        save_tasks(tasks, path)
        assert load_tasks(path) == tasks

    def test_overwrites_existing_file(self, tmp_path):
        """save_tasks replaces the file contents on each call."""
        path = tmp_path / "tasks.json"
        save_tasks([{"id": 1, "title": "Old task", "status": "pending", "created_at": "2026-04-03T08:00:00"}], path)
        save_tasks([], path)
        assert load_tasks(path) == []

    def test_json_is_indented(self, tmp_path):
        """Output JSON uses 2-space indentation (per CLAUDE.md convention)."""
        path = tmp_path / "tasks.json"
        save_tasks([{"id": 1, "title": "Check indent", "status": "pending", "created_at": "2026-04-03T10:00:00"}], path)
        raw = path.read_text()
        assert "  " in raw  # 2-space indent present
