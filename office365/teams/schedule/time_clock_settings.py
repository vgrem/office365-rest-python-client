from __future__ import annotations

from dataclasses import field

from office365.onedrive.driveitems.geo_coordinates import GeoCoordinates
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class TimeClockSettings(ClientValue):
    approvedLocation: GeoCoordinates = field(default_factory=GeoCoordinates)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TimeClockSettings"
