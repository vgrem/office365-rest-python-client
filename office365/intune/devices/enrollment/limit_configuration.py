from __future__ import annotations

from typing import Optional

from office365.intune.devices.enrollment.configuration import (
    DeviceEnrollmentConfiguration,
)
from office365.runtime.types.odata_property import odata


class DeviceEnrollmentLimitConfiguration(DeviceEnrollmentConfiguration):
    """Device Enrollment Configuration that restricts the number of devices a user can enroll"""

    @odata(name="limit")
    @property
    def limit(self) -> Optional[int]:
        """Gets the limit property"""
        return self.properties.get("limit", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceEnrollmentLimitConfiguration"
