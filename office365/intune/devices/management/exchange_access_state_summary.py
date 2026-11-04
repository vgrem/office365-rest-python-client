from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class DeviceExchangeAccessStateSummary(ClientValue):
    allowedDeviceCount: int | None = None
    blockedDeviceCount: int | None = None
    quarantinedDeviceCount: int | None = None
    unavailableDeviceCount: int | None = None
    unknownDeviceCount: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceExchangeAccessStateSummary"
