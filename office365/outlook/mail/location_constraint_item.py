from __future__ import annotations

from office365.outlook.mail.location import Location
from office365.runtime.types.value import value


@value
class LocationConstraintItem(Location):
    resolveAvailability: bool | None = None
    "The conditions stated by a client for the location of a meeting."

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.LocationConstraintItem"
