from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class AppsInstallationOptionsForMac(ClientValue):
    isMicrosoft365AppsEnabled: bool | None = None
    isSkypeForBusinessEnabled: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AppsInstallationOptionsForMac"
