from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.management.enrollment_platform_restriction import (
        DeviceEnrollmentPlatformRestriction,
    )


class DeviceEnrollmentPlatformRestrictionsConfiguration(Entity):
    @odata(name="androidRestriction")
    @property
    def android_restriction(self) -> DeviceEnrollmentPlatformRestriction:
        """Gets the androidRestriction property"""
        from office365.intune.devices.management.enrollment_platform_restriction import (
            DeviceEnrollmentPlatformRestriction,
        )

        return self.properties.get("androidRestriction", DeviceEnrollmentPlatformRestriction())

    @odata(name="iosRestriction")
    @property
    def ios_restriction(self) -> DeviceEnrollmentPlatformRestriction:
        """Gets the iosRestriction property"""
        from office365.intune.devices.management.enrollment_platform_restriction import (
            DeviceEnrollmentPlatformRestriction,
        )

        return self.properties.get("iosRestriction", DeviceEnrollmentPlatformRestriction())

    @odata(name="macOSRestriction")
    @property
    def mac_os_restriction(self) -> DeviceEnrollmentPlatformRestriction:
        """Gets the macOSRestriction property"""
        from office365.intune.devices.management.enrollment_platform_restriction import (
            DeviceEnrollmentPlatformRestriction,
        )

        return self.properties.get("macOSRestriction", DeviceEnrollmentPlatformRestriction())

    @odata(name="windowsMobileRestriction")
    @property
    def windows_mobile_restriction(self) -> DeviceEnrollmentPlatformRestriction:
        """Gets the windowsMobileRestriction property"""
        from office365.intune.devices.management.enrollment_platform_restriction import (
            DeviceEnrollmentPlatformRestriction,
        )

        return self.properties.get("windowsMobileRestriction", DeviceEnrollmentPlatformRestriction())

    @odata(name="windowsRestriction")
    @property
    def windows_restriction(self) -> DeviceEnrollmentPlatformRestriction:
        """Gets the windowsRestriction property"""
        from office365.intune.devices.management.enrollment_platform_restriction import (
            DeviceEnrollmentPlatformRestriction,
        )

        return self.properties.get("windowsRestriction", DeviceEnrollmentPlatformRestriction())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceEnrollmentPlatformRestrictionsConfiguration"
