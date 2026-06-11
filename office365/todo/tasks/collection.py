from __future__ import annotations

from datetime import datetime

from office365.delta_collection import DeltaCollection
from office365.outlook.calendar.dateTimeTimeZone import DateTimeTimeZone
from office365.outlook.mail.importance import Importance
from office365.outlook.mail.item_body import ItemBody
from office365.todo.tasks.task import TodoTask


class TodoTaskCollection(DeltaCollection[TodoTask]):
    """ """

    def __init__(self, context, resource_path=None):
        super().__init__(context, TodoTask, resource_path)

    def add(
        self,
        title: str,
        due_date_time: datetime | DateTimeTimeZone | str | None = None,
        importance: Importance | None = None,
        body: str | ItemBody | None = None,
        **kwargs,
    ):
        kwargs["title"] = title

        if due_date_time is not None:
            if isinstance(due_date_time, datetime):
                kwargs["dueDateTime"] = DateTimeTimeZone.parse(due_date_time)
            elif isinstance(due_date_time, DateTimeTimeZone):
                kwargs["dueDateTime"] = due_date_time
            else:
                kwargs["dueDateTime"] = due_date_time

        if importance is not None:
            kwargs["importance"] = importance

        if body is not None:
            if isinstance(body, str):
                kwargs["body"] = ItemBody.text(body)
            elif isinstance(body, ItemBody):
                kwargs["body"] = body

        return super().add(**kwargs)  # type: ignore[arg-type]
