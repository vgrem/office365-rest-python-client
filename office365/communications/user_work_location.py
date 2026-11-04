from __future__ import annotations

from office365.communications.presences.work_location_source import WorkLocationSource
from office365.communications.presences.work_location_type import WorkLocationType
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class UserWorkLocation(ClientValue):
    placeId: str | None = None
    source: WorkLocationSource = WorkLocationSource.none
    workLocationType: WorkLocationType = WorkLocationType.unspecified

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserWorkLocation"
