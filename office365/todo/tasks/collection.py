from __future__ import annotations

from office365.delta_collection import DeltaCollection
from office365.outlook.mail.importance import Importance
from office365.todo.tasks.task import TodoTask


class TodoTaskCollection(DeltaCollection[TodoTask]):
    """ """

    def __init__(self, context, resource_path=None):
        super().__init__(context, TodoTask, resource_path)

    def add(self, title: str, due_date_time: str | None, importance: Importance | None, body: str | None = None):
        super().add(title=title, dueDateTime=due_date_time, importance=importance, body=body)


