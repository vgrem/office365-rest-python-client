from __future__ import annotations

from datetime import datetime

from office365.delta_collection import DeltaCollection
from office365.outlook.calendar.dateTimeTimeZone import DateTimeTimeZone
from office365.outlook.mail.importance import Importance
from office365.outlook.mail.item_body import ItemBody
from office365.runtime.paths.v4.entity import EntityPath
from office365.runtime.queries.create_entity import CreateEntityQuery
from office365.todo.tasks.task import TodoTask


class TodoTaskCollection(DeltaCollection[TodoTask]):
    """ """

    def __init__(self, context, resource_path=None):
        super().__init__(context, TodoTask, resource_path)

    def add(
        self,
        title: str,
        due_date_time: datetime | DateTimeTimeZone | None = None,
        importance: Importance | None = None,
        body: str | ItemBody | None = None,
        **kwargs,
    ):
        return_type = TodoTask(self.context, EntityPath(None, self.resource_path))
        return_type.set_property("title", title)

        if due_date_time is not None:
            if isinstance(due_date_time, datetime):
                return_type.set_property("dueDateTime", DateTimeTimeZone.parse(due_date_time))
            elif isinstance(due_date_time, DateTimeTimeZone):
                return_type.set_property("dueDateTime", due_date_time)
            elif isinstance(due_date_time, datetime):
                return_type.set_property("dueDateTime", DateTimeTimeZone.parse(due_date_time))

        if importance is not None:
            return_type.set_property("importance", importance)

        if body is not None:
            if isinstance(body, str):
                return_type.set_property("body", ItemBody.text(body))
            elif isinstance(body, ItemBody):
                return_type.set_property("body", body)

        qry = CreateEntityQuery(self, return_type.to_json(), return_type)
        self.context.add_query(qry)
        return return_type
