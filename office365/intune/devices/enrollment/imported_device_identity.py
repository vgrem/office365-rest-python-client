from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.intune.devices.management.enrollment_state import EnrollmentState
from office365.runtime.types.odata_property import odata, version


@version("beta")
class ImportedDeviceIdentity(Entity):
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

    @odata(name="enrollmentState")
    @property
    def enrollment_state(self) -> EnrollmentState:
        """Gets the enrollmentState property"""
        return self.properties.get("enrollmentState", EnrollmentState.unknown)

    @odata(name="importedDeviceIdentifier")
    @property
    def imported_device_identifier(self) -> Optional[str]:
        """Gets the importedDeviceIdentifier property"""
        return self.properties.get("importedDeviceIdentifier", None)

    @odata(name="lastContactedDateTime")
    @property
    def last_contacted_date_time(self) -> Optional[datetime]:
        """Gets the lastContactedDateTime property"""
        return self.properties.get("lastContactedDateTime", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ImportedDeviceIdentity"
