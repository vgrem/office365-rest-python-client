from __future__ import annotations

from office365.runtime.client_value import ClientValue


class AppsInstallationOptionsForWindows(ClientValue):
    isMicrosoft365AppsEnabled: bool | None = None
    isProjectEnabled: bool | None = None
    isSkypeForBusinessEnabled: bool | None = None
    isVisioEnabled: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AppsInstallationOptionsForWindows"
