from __future__ import annotations

from datetime import datetime
from typing import Optional

from typing_extensions import Self

from office365.entity import Entity
from office365.intune.devices.management.app_management_task_category import DeviceAppManagementTaskCategory
from office365.intune.devices.management.app_management_task_priority import DeviceAppManagementTaskPriority
from office365.intune.devices.management.app_management_task_status import DeviceAppManagementTaskStatus
from office365.permissions import require_permission
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata, version


@version("beta")
class DeviceAppManagementTask(Entity):
    @odata(name="assignedTo")
    @property
    def assigned_to(self) -> Optional[str]:
        """Gets the assignedTo property"""
        return self.properties.get("assignedTo", None)

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", None)

    @odata(name="creator")
    @property
    def creator(self) -> Optional[str]:
        """Gets the creator property"""
        return self.properties.get("creator", None)

    @odata(name="creatorNotes")
    @property
    def creator_notes(self) -> Optional[str]:
        """Gets the creatorNotes property"""
        return self.properties.get("creatorNotes", None)

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="dueDateTime")
    @property
    def due_date_time(self) -> Optional[datetime]:
        """Gets the dueDateTime property"""
        return self.properties.get("dueDateTime", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceAppManagementTask"

    @odata(name="status")
    @property
    def status(self) -> Optional[DeviceAppManagementTaskStatus]:
        """Gets the status property"""
        return self.properties.get("status", None)

    @require_permission(
        delegated=[
            "DeviceManagementApps.ReadWrite.All",
        ],
        application=[
            "DeviceManagementApps.ReadWrite.All",
        ],
    )
    def update_status(self, status: DeviceAppManagementTaskStatus, note: str) -> Self:
        """updateStatus operation.

        Args:
            status (DeviceAppManagementTaskStatus):
                status parameter
            note (str):
                note parameter
        """
        qry = ServiceOperationQuery(self, "updateStatus", None, {"status": status, "note": note}, None, None)
        self.context.add_query(qry)
        return self

    @odata(name="category")
    @property
    def category(self) -> Optional[DeviceAppManagementTaskCategory]:
        """Gets the category property"""
        return self.properties.get("category", None)

    @odata(name="priority")
    @property
    def priority(self) -> Optional[DeviceAppManagementTaskPriority]:
        """Gets the priority property"""
        return self.properties.get("priority", None)
