from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class AuthenticationAppDeviceDetails(ClientValue):
    appVersion: str | None = None
    clientApp: str | None = None
    deviceId: str | None = None
    operatingSystem: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AuthenticationAppDeviceDetails"
