from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.enrollment.configuration_assignment import (
        EnrollmentConfigurationAssignment,
    )


class DeviceEnrollmentConfiguration(Entity):
    """The Base Class of Device Enrollment Configuration"""

    def __str__(self):
        return self.display_name or self.entity_type_name

    @odata(name="createdDateTime")
    @property
    def created_datetime(self) -> datetime:
        """
        Created date time in UTC of the device enrollment configuration
        """
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """The display name of the device enrollment configuration"""
        return self.properties.get("displayName", None)

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @odata(name="priority")
    @property
    def priority(self) -> Optional[int]:
        """Gets the priority property"""
        return self.properties.get("priority", None)

    @odata(name="version")
    @property
    def version(self) -> Optional[int]:
        """Gets the version property"""
        return self.properties.get("version", None)

    @odata(name="assignments", navigation=True)
    @property
    def assignments(self) -> EntityCollection[EnrollmentConfigurationAssignment]:
        """Gets the assignments property"""
        from office365.intune.devices.enrollment.configuration_assignment import (
            EnrollmentConfigurationAssignment,
        )

        return self.properties.get(
            "assignments",
            EntityCollection[EnrollmentConfigurationAssignment](
                self.context, EnrollmentConfigurationAssignment, ResourcePath("assignments", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceEnrollmentConfiguration"
