from __future__ import annotations

from dataclasses import dataclass, field

from office365.intune.devices.operating_system_specifications import OperatingSystemSpecifications
from office365.runtime.client_value import ClientValue


@dataclass
class DeviceMetadata(ClientValue):
    deviceType: str | None = None
    ipAddress: str | None = None
    operatingSystemSpecifications: OperatingSystemSpecifications = field(default_factory=OperatingSystemSpecifications)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceMetadata"
