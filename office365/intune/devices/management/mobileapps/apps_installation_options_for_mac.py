from __future__ import annotations

from office365.runtime.client_value import ClientValue


class AppsInstallationOptionsForMac(ClientValue):
    isMicrosoft365AppsEnabled: bool | None = None
    isSkypeForBusinessEnabled: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AppsInstallationOptionsForMac"
