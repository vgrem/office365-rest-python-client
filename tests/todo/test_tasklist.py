from __future__ import annotations

from typing import Optional

from office365.todo.tasks.list import TodoTaskList
from tests import create_unique_name
from tests.decorators import requires_delegated_permission_or_role
from tests.graph_case import GraphDelegatedTestCase


class TestTaskList(GraphDelegatedTestCase):
    task_list: Optional[TodoTaskList] = None

    @requires_delegated_permission_or_role("Tasks.ReadWrite", roles=["Global Administrator"])
    def test1_create_task_list(self):
        """Creates a task list"""
        name = create_unique_name("TaskList")
        task_list = self.client.me.todo.lists.add(name).execute_query()
        TestTaskList.task_list = task_list

    @requires_delegated_permission_or_role("Tasks.Read", "Tasks.ReadWrite", roles=["Global Administrator"])
    def test2_get_task_lists(self):
        """Gets all task lists"""
        task_lists = self.client.me.todo.lists.get().execute_query()
        self.assertIsNotNone(task_lists.resource_path)

    @requires_delegated_permission_or_role("Tasks.ReadWrite", roles=["Global Administrator"])
    def test3_create_task(self):
        """Creates a task in the task list"""
        assert TestTaskList.task_list is not None, "Task list must be created"
        task = TestTaskList.task_list.tasks.add(title="A new task").execute_query()
        self.assertIsNotNone(task.resource_path)

    @requires_delegated_permission_or_role("Tasks.Read", "Tasks.ReadWrite", roles=["Global Administrator"])
    def test4_list_tasks(self):
        """Lists all tasks in the task list"""
        assert TestTaskList.task_list is not None, "Task list must be created"
        tasks = TestTaskList.task_list.tasks.get().execute_query()
        self.assertIsNotNone(tasks.resource_path)
        self.assertGreater(len(tasks), 0)

    @requires_delegated_permission_or_role("Tasks.ReadWrite", roles=["Global Administrator"])
    def test5_delete_task_list(self):
        """Deletes the task list"""
        assert TestTaskList.task_list is not None, "Task list must be created"
        list_to_del = TestTaskList.task_list
        list_to_del.delete_object().execute_query()
