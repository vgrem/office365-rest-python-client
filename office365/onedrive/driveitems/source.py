from __future__ import annotations

from office365.onedrive.driveitems.sourceapplication import DriveItemSourceApplication
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class DriveItemSource(ClientValue):
    application: DriveItemSourceApplication = DriveItemSourceApplication.teams
    externalId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DriveItemSource"
