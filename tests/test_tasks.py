"""Tests for task creation logic (src/tasks.py).

All tests here cover AC-1: adding a task creates a valid task record.
These tests are written before any implementation exists and should fail
with ImportError until src/tasks.py is written.
"""

import pytest
from src.tasks import create_task


class TestCreateTask:
    def test_returns_dict(self):
        """create_task returns a dictionary."""
        task = create_task(id=1, title="Buy milk")
        assert isinstance(task, dict)

    def test_title_is_stored(self):
        """The title passed in is preserved exactly."""
        task = create_task(id=1, title="Buy milk")
        assert task["title"] == "Buy milk"

    def test_id_is_stored(self):
        """The id passed in is stored as an integer."""
        task = create_task(id=3, title="Walk dog")
        assert task["id"] == 3
        assert isinstance(task["id"], int)

    def test_default_status_is_pending(self):
        """A new task starts with status 'pending'."""
        task = create_task(id=1, title="Buy milk")
        assert task["status"] == "pending"

    def test_created_at_is_iso_string(self):
        """created_at is an ISO 8601 datetime string."""
        from datetime import datetime
        task = create_task(id=1, title="Buy milk")
        assert "created_at" in task
        # Must be parseable as a datetime
        parsed = datetime.fromisoformat(task["created_at"])
        assert isinstance(parsed, datetime)

    def test_empty_title_raises(self):
        """An empty title is rejected with a ValueError."""
        with pytest.raises(ValueError):
            create_task(id=1, title="")

    def test_whitespace_only_title_raises(self):
        """A whitespace-only title is rejected with a ValueError."""
        with pytest.raises(ValueError):
            create_task(id=1, title="   ")
