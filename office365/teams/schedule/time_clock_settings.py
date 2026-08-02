from __future__ import annotations

from dataclasses import dataclass, field

from office365.onedrive.driveitems.geo_coordinates import GeoCoordinates
from office365.runtime.client_value import ClientValue


@dataclass
class TimeClockSettings(ClientValue):
    approvedLocation: GeoCoordinates = field(default_factory=GeoCoordinates)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TimeClockSettings"
