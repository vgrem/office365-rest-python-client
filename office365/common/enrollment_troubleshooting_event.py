from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.intune.devices.enrollment.failurereason import DeviceEnrollmentFailureReason
from office365.intune.devices.enrollment.type import DeviceEnrollmentType
from office365.runtime.types.odata_property import odata


class EnrollmentTroubleshootingEvent(Entity):
    @odata(name="deviceId")
    @property
    def device_id(self) -> Optional[str]:
        """Gets the deviceId property"""
        return self.properties.get("deviceId", None)

    @odata(name="enrollmentType")
    @property
    def enrollment_type(self) -> DeviceEnrollmentType:
        """Gets the enrollmentType property"""
        return self.properties.get("enrollmentType", DeviceEnrollmentType.unknown)

    @odata(name="failureCategory")
    @property
    def failure_category(self) -> DeviceEnrollmentFailureReason:
        """Gets the failureCategory property"""
        return self.properties.get("failureCategory", DeviceEnrollmentFailureReason.unknown)

    @odata(name="failureReason")
    @property
    def failure_reason(self) -> Optional[str]:
        """Gets the failureReason property"""
        return self.properties.get("failureReason", None)

    @odata(name="managedDeviceIdentifier")
    @property
    def managed_device_identifier(self) -> Optional[str]:
        """Gets the managedDeviceIdentifier property"""
        return self.properties.get("managedDeviceIdentifier", None)

    @odata(name="operatingSystem")
    @property
    def operating_system(self) -> Optional[str]:
        """Gets the operatingSystem property"""
        return self.properties.get("operatingSystem", None)

    @odata(name="osVersion")
    @property
    def os_version(self) -> Optional[str]:
        """Gets the osVersion property"""
        return self.properties.get("osVersion", None)

    @odata(name="userId")
    @property
    def user_id(self) -> Optional[str]:
        """Gets the userId property"""
        return self.properties.get("userId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.EnrollmentTroubleshootingEvent"
