from __future__ import annotations

from office365.runtime.client_value import ClientValue


class WindowsDeviceADAccount(ClientValue):
    domainName: str | None = None
    userName: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsDeviceADAccount"
