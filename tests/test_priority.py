"""Tests for priority support in src/tasks.py (Level 1 — single-file area).

Covers: priority field on create_task, sort_by_priority, filter_by_priority.
Written before implementation — fails with ImportError until tasks.py is updated.
"""

import pytest
from src.tasks import create_task, filter_by_priority, sort_by_priority


class TestCreateTaskPriority:
    def test_default_priority_is_medium(self):
        task = create_task(id=1, title="A")
        assert task["priority"] == "medium"

    def test_explicit_priority_low(self):
        task = create_task(id=1, title="A", priority="low")
        assert task["priority"] == "low"

    def test_explicit_priority_high(self):
        task = create_task(id=1, title="A", priority="high")
        assert task["priority"] == "high"

    def test_invalid_priority_raises_value_error(self):
        with pytest.raises(ValueError, match="priority"):
            create_task(id=1, title="A", priority="urgent")

    def test_priority_stored_in_task_dict(self):
        task = create_task(id=1, title="A", priority="low")
        assert "priority" in task


class TestSortByPriority:
    def test_high_sorted_before_medium(self):
        tasks = [
            create_task(id=1, title="Med", priority="medium"),
            create_task(id=2, title="High", priority="high"),
        ]
        result = sort_by_priority(tasks)
        assert result[0]["id"] == 2

    def test_medium_sorted_before_low(self):
        tasks = [
            create_task(id=1, title="Low", priority="low"),
            create_task(id=2, title="Med", priority="medium"),
        ]
        result = sort_by_priority(tasks)
        assert result[0]["id"] == 2

    def test_high_medium_low_full_order(self):
        tasks = [
            create_task(id=1, title="Low", priority="low"),
            create_task(id=2, title="High", priority="high"),
            create_task(id=3, title="Med", priority="medium"),
        ]
        result = sort_by_priority(tasks)
        assert [t["id"] for t in result] == [2, 3, 1]

    def test_returns_all_tasks(self):
        tasks = [create_task(id=i, title=f"T{i}", priority="medium") for i in range(1, 4)]
        assert len(sort_by_priority(tasks)) == 3

    def test_does_not_mutate_original_list(self):
        tasks = [
            create_task(id=1, title="Low", priority="low"),
            create_task(id=2, title="High", priority="high"),
        ]
        sort_by_priority(tasks)
        assert tasks[0]["id"] == 1

    def test_returns_list_type(self):
        assert isinstance(sort_by_priority([]), list)


class TestFilterByPriority:
    def test_returns_only_matching_priority(self):
        tasks = [
            create_task(id=1, title="High", priority="high"),
            create_task(id=2, title="Low", priority="low"),
        ]
        result = filter_by_priority(tasks, "high")
        assert len(result) == 1
        assert result[0]["id"] == 1

    def test_returns_empty_when_no_match(self):
        tasks = [create_task(id=1, title="A", priority="medium")]
        assert filter_by_priority(tasks, "high") == []

    def test_returns_all_when_all_match(self):
        tasks = [create_task(id=i, title=f"T{i}", priority="low") for i in range(1, 4)]
        assert len(filter_by_priority(tasks, "low")) == 3

    def test_returns_list_type(self):
        assert isinstance(filter_by_priority([], "medium"), list)
