"""Tests for mark_done and next_id (src/tasks.py).

Covers AC-3 (marking a task done) and AC-5 (invalid ID handling).
Written before implementation — should fail with ImportError until
mark_done and next_id are added to src/tasks.py.
"""

import pytest
from src.tasks import create_task, mark_done, next_id


class TestNextId:
    def test_returns_one_for_empty_list(self):
        """next_id returns 1 when no tasks exist."""
        assert next_id([]) == 1

    def test_returns_one_more_than_max(self):
        """next_id returns max existing id + 1."""
        tasks = [create_task(id=1, title="A"), create_task(id=3, title="B")]
        assert next_id(tasks) == 4

    def test_returns_int(self):
        """next_id always returns an integer."""
        assert isinstance(next_id([]), int)


class TestMarkDone:
    def test_changes_status_to_done(self):
        """mark_done sets the task status to 'done'."""
        tasks = [create_task(id=1, title="Buy milk")]
        mark_done(tasks, 1)
        assert tasks[0]["status"] == "done"

    def test_returns_the_task_list(self):
        """mark_done returns the task list."""
        tasks = [create_task(id=1, title="Buy milk")]
        result = mark_done(tasks, 1)
        assert isinstance(result, list)

    def test_preserves_title(self):
        """mark_done does not alter the task title."""
        tasks = [create_task(id=1, title="Buy milk")]
        mark_done(tasks, 1)
        assert tasks[0]["title"] == "Buy milk"

    def test_preserves_created_at(self):
        """mark_done does not alter the created_at timestamp."""
        tasks = [create_task(id=1, title="Buy milk")]
        original_ts = tasks[0]["created_at"]
        mark_done(tasks, 1)
        assert tasks[0]["created_at"] == original_ts

    def test_only_marks_target_task(self):
        """mark_done only changes the specified task, not others."""
        tasks = [create_task(id=1, title="A"), create_task(id=2, title="B")]
        mark_done(tasks, 1)
        assert tasks[1]["status"] == "pending"

    def test_raises_for_missing_id(self):
        """mark_done raises ValueError when the task ID does not exist."""
        tasks = [create_task(id=1, title="Buy milk")]
        with pytest.raises(ValueError, match="99"):
            mark_done(tasks, 99)

    def test_does_not_modify_list_on_missing_id(self):
        """mark_done does not change any task when the ID is not found."""
        tasks = [create_task(id=1, title="Buy milk")]
        try:
            mark_done(tasks, 99)
        except ValueError:
            pass
        assert tasks[0]["status"] == "pending"
