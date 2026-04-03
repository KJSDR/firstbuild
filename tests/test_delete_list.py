"""Tests for delete_task and list_tasks (src/tasks.py).

Covers AC-2 (listing by status), AC-4 (delete), and AC-5 (invalid ID).
Written before implementation — should fail with ImportError until
delete_task and list_tasks are added to src/tasks.py.
"""

import pytest
from src.tasks import create_task, delete_task, list_tasks


class TestDeleteTask:
    def test_removes_target_task(self):
        """delete_task removes the task with the given ID."""
        tasks = [create_task(id=1, title="A"), create_task(id=2, title="B")]
        result = delete_task(tasks, 1)
        assert all(t["id"] != 1 for t in result)

    def test_returns_remaining_tasks(self):
        """delete_task returns a list containing all other tasks."""
        tasks = [create_task(id=1, title="A"), create_task(id=2, title="B")]
        result = delete_task(tasks, 1)
        assert len(result) == 1
        assert result[0]["id"] == 2

    def test_returns_empty_list_when_last_task_deleted(self):
        """delete_task returns [] when the only task is deleted."""
        tasks = [create_task(id=1, title="A")]
        result = delete_task(tasks, 1)
        assert result == []

    def test_returns_list_type(self):
        """delete_task always returns a list."""
        tasks = [create_task(id=1, title="A")]
        result = delete_task(tasks, 1)
        assert isinstance(result, list)

    def test_does_not_mutate_original_list(self):
        """delete_task does not modify the original task list."""
        tasks = [create_task(id=1, title="A"), create_task(id=2, title="B")]
        delete_task(tasks, 1)
        assert len(tasks) == 2

    def test_raises_for_missing_id(self):
        """delete_task raises ValueError when the task ID does not exist."""
        tasks = [create_task(id=1, title="A")]
        with pytest.raises(ValueError, match="99"):
            delete_task(tasks, 99)

    def test_raises_on_empty_list(self):
        """delete_task raises ValueError when the task list is empty."""
        with pytest.raises(ValueError):
            delete_task([], 1)


class TestListTasks:
    def test_returns_all_tasks_when_no_filter(self):
        """list_tasks returns all tasks when status is None."""
        tasks = [create_task(id=1, title="A"), create_task(id=2, title="B")]
        result = list_tasks(tasks)
        assert len(result) == 2

    def test_filters_pending(self):
        """list_tasks returns only pending tasks when status='pending'."""
        tasks = [create_task(id=1, title="A"), create_task(id=2, title="B")]
        tasks[1]["status"] = "done"
        result = list_tasks(tasks, status="pending")
        assert len(result) == 1
        assert result[0]["id"] == 1

    def test_filters_done(self):
        """list_tasks returns only done tasks when status='done'."""
        tasks = [create_task(id=1, title="A"), create_task(id=2, title="B")]
        tasks[0]["status"] = "done"
        result = list_tasks(tasks, status="done")
        assert len(result) == 1
        assert result[0]["id"] == 1

    def test_returns_empty_list_when_no_match(self):
        """list_tasks returns [] when no tasks match the filter."""
        tasks = [create_task(id=1, title="A")]
        result = list_tasks(tasks, status="done")
        assert result == []

    def test_returns_empty_list_for_empty_input(self):
        """list_tasks returns [] when given an empty task list."""
        assert list_tasks([]) == []
        assert list_tasks([], status="pending") == []

    def test_returns_list_type(self):
        """list_tasks always returns a list."""
        result = list_tasks([])
        assert isinstance(result, list)
