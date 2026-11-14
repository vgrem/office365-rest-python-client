from __future__ import annotations

from datetime import datetime
from typing import Optional

from typing_extensions import Self

from office365.entity import Entity
from office365.intune.devices.platformtype import DevicePlatformType
from office365.permissions import require_permission
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata, version


@version("beta")
class AppleUserInitiatedEnrollmentProfile(Entity):
    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", None)

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

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", None)

    @odata(name="platform")
    @property
    def platform(self) -> DevicePlatformType:
        """Gets the platform property"""
        return self.properties.get("platform", DevicePlatformType.android)

    @odata(name="priority")
    @property
    def priority(self) -> Optional[int]:
        """Gets the priority property"""
        return self.properties.get("priority", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AppleUserInitiatedEnrollmentProfile"

    @require_permission(
        delegated=[
            "DeviceManagementServiceConfig.ReadWrite.All",
        ],
        application=[
            "DeviceManagementServiceConfig.ReadWrite.All",
        ],
    )
    def set_priority(self, priority: int) -> Self:
        """setPriority operation.

        Args:
            priority (int):
                priority parameter
        """
        qry = ServiceOperationQuery(self, "setPriority", None, {"priority": priority}, None, None)
        self.context.add_query(qry)
        return self
