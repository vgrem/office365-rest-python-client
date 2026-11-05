from __future__ import annotations

from office365.runtime.client_value import ClientValue


class DeviceEnrollmentPlatformRestriction(ClientValue):
    osMaximumVersion: str | None = None
    osMinimumVersion: str | None = None
    personalDeviceEnrollmentBlocked: bool | None = None
    platformBlocked: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceEnrollmentPlatformRestriction"
