from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.directory.extensions.extension import Extension
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.intune.print.taskstatus import TaskStatus
from office365.outlook.calendar.dateTimeTimeZone import DateTimeTimeZone
from office365.outlook.mail.importance import Importance
from office365.outlook.mail.item_body import ItemBody
from office365.outlook.mail.patterned_recurrence import PatternedRecurrence
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata
from office365.todo.attachments.base import AttachmentBase
from office365.todo.attachments.session import AttachmentSession
from office365.todo.checklist_item import ChecklistItem
from office365.todo.linked_resource import LinkedResource


class TodoTask(Entity):
    """A todoTask represents a task, such as a piece of work or personal item, that can be tracked and completed."""

    def __str__(self) -> str:
        return self.title or self.entity_type_name or ""

    @property
    def body(self) -> ItemBody:
        """The task body that typically contains information about the task."""
        return self.properties.get("body", ItemBody())

    @odata(name="bodyLastModifiedDateTime")
    @property
    def body_last_modified_date_time(self) -> Optional[datetime]:
        """The date and time when the task body was last modified."""
        return self.properties.get("bodyLastModifiedDateTime", None)

    @odata(name="categories")
    @property
    def categories(self) -> StringCollection:
        """The categories associated with the task."""
        return self.properties.get("categories", StringCollection())

    @odata(name="completedDateTime")
    @property
    def completed_date_time(self) -> Optional[DateTimeTimeZone]:
        """The date and time when the task was completed."""
        return self.properties.get("completedDateTime", None)

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """The date and time when the task was created."""
        return self.properties.get("createdDateTime", None)

    @odata(name="dueDateTime")
    @property
    def due_date_time(self) -> Optional[DateTimeTimeZone]:
        """The date and time when the task is due."""
        return self.properties.get("dueDateTime", None)

    @odata(name="hasAttachments")
    @property
    def has_attachments(self) -> Optional[bool]:
        """Indicates whether the task has attachments."""
        return self.properties.get("hasAttachments", None)

    @odata(name="importance")
    @property
    def importance(self) -> Optional[Importance]:
        """The importance of the task. Possible values: low, normal, high."""
        return self.properties.get("importance", None)

    @odata(name="isReminderOn")
    @property
    def is_reminder_on(self) -> Optional[bool]:
        """Indicates whether a reminder is on for the task."""
        return self.properties.get("isReminderOn", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """The date and time when the task was last modified."""
        return self.properties.get("lastModifiedDateTime", None)

    @odata(name="recurrence")
    @property
    def recurrence(self) -> Optional[PatternedRecurrence]:
        """The recurrence pattern for the task."""
        return self.properties.get("recurrence", None)

    @odata(name="reminderDateTime")
    @property
    def reminder_date_time(self) -> Optional[DateTimeTimeZone]:
        """The date and time for the reminder of the task."""
        return self.properties.get("reminderDateTime", None)

    @odata(name="startDateTime")
    @property
    def start_date_time(self) -> Optional[DateTimeTimeZone]:
        """The date and time when the task is scheduled to start."""
        return self.properties.get("startDateTime", None)

    @odata(name="status")
    @property
    def status(self) -> Optional[TaskStatus]:
        """The status of the task. Possible values: notStarted, inProgress, completed, waitingOnOthers, deferred."""
        return self.properties.get("status", None)

    @property
    def title(self) -> Optional[str]:
        """A brief description of the task."""
        return self.properties.get("title", None)

    @title.setter
    def title(self, value):
        self.set_property("title", value)

    @property
    def attachment_sessions(self) -> EntityCollection[AttachmentSession]:
        """A collection of attachment sessions for the task."""
        return self.properties.get(
            "attachmentSessions",
            EntityCollection(
                self.context,
                AttachmentSession,
                ResourcePath("attachmentSessions", self.resource_path),
            ),
        )

    @property
    def attachments(self) -> EntityCollection[AttachmentBase]:
        """A collection of file attachments for the task."""
        return self.properties.get(
            "attachments",
            EntityCollection(
                self.context,
                AttachmentBase,
                ResourcePath("attachments", self.resource_path),
            ),
        )

    @property
    def extensions(self) -> EntityCollection[Extension]:
        """The collection of open extensions defined for the task."""
        return self.properties.get(
            "extensions",
            EntityCollection(self.context, Extension, ResourcePath("extensions", self.resource_path)),
        )

    @odata(name="checklistItems")
    @property
    def checklist_items(self) -> EntityCollection[ChecklistItem]:
        """A collection of checklistItems linked to a task."""
        return self.properties.get(
            "checklistItems",
            EntityCollection(
                self.context,
                ChecklistItem,
                ResourcePath("checklistItems", self.resource_path),
            ),
        )

    @odata(name="linkedResources")
    @property
    def linked_resources(self) -> EntityCollection[LinkedResource]:
        """A collection of resources linked to the task."""
        return self.properties.get(
            "linkedResources",
            EntityCollection(
                self.context,
                LinkedResource,
                ResourcePath("linkedResources", self.resource_path),
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return None  # type: ignore
