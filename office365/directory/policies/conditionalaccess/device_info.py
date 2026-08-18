from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class DeviceInfo(ClientValue):
    deviceId: str | None = None
    displayName: str | None = None
    enrollmentProfileName: str | None = None
    extensionAttribute1: str | None = None
    extensionAttribute10: str | None = None
    extensionAttribute11: str | None = None
    extensionAttribute12: str | None = None
    extensionAttribute13: str | None = None
    extensionAttribute14: str | None = None
    extensionAttribute15: str | None = None
    extensionAttribute2: str | None = None
    extensionAttribute3: str | None = None
    extensionAttribute4: str | None = None
    extensionAttribute5: str | None = None
    extensionAttribute6: str | None = None
    extensionAttribute7: str | None = None
    extensionAttribute8: str | None = None
    extensionAttribute9: str | None = None
    isCompliant: bool | None = None
    manufacturer: str | None = None
    mdmAppId: str | None = None
    model: str | None = None
    operatingSystem: str | None = None
    operatingSystemVersion: str | None = None
    ownership: str | None = None
    physicalIds: StringCollection = field(default_factory=StringCollection)
    profileType: str | None = None
    systemLabels: StringCollection = field(default_factory=StringCollection)
    trustType: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceInfo"
