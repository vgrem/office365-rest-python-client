from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class AuthenticationAppDeviceDetails(ClientValue):
    appVersion: str | None = None
    clientApp: str | None = None
    deviceId: str | None = None
    operatingSystem: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AuthenticationAppDeviceDetails"
