from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.security.coachmark_location_type import CoachmarkLocationType


class CoachmarkLocation(ClientValue):
    length: int | None = None
    offset: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CoachmarkLocation"

    type: CoachmarkLocationType = CoachmarkLocationType.unknown
