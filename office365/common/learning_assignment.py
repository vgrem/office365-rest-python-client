from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.directory.applications.assignmenttype import AssignmentType
from office365.entity import Entity
from office365.outlook.calendar.dateTimeTimeZone import DateTimeTimeZone
from office365.outlook.mail.item_body import ItemBody
from office365.runtime.types.odata_property import odata


class LearningAssignment(Entity):
    @odata(name="assignedDateTime")
    @property
    def assigned_date_time(self) -> Optional[datetime]:
        """Gets the assignedDateTime property"""
        return self.properties.get("assignedDateTime", datetime.min)

    @odata(name="assignerUserId")
    @property
    def assigner_user_id(self) -> Optional[str]:
        """Gets the assignerUserId property"""
        return self.properties.get("assignerUserId", None)

    @odata(name="assignmentType")
    @property
    def assignment_type(self) -> AssignmentType:
        """Gets the assignmentType property"""
        return self.properties.get("assignmentType", AssignmentType.required)

    @odata(name="dueDateTime")
    @property
    def due_date_time(self) -> DateTimeTimeZone:
        """Gets the dueDateTime property"""
        return self.properties.get("dueDateTime", DateTimeTimeZone())

    @odata(name="notes")
    @property
    def notes(self) -> ItemBody:
        """Gets the notes property"""
        return self.properties.get("notes", ItemBody())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.LearningAssignment"
