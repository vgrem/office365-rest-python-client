from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class GeoCoordinates(ClientValue):
    """
    The GeoCoordinates resource provides geographic coordinates and elevation of a location based on metadata
    contained within the file. If a DriveItem has a non-null location facet, the item represents a file with
    a known location associated with it.
    """

    altitude: float | None = None
    latitude: float | None = None
    longitude: float | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.GeoCoordinates"
