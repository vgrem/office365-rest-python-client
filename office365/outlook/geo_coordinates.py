from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class OutlookGeoCoordinates(ClientValue):
    """The geographic coordinates, elevation, and their degree of accuracy for a physical location.

    Fields:
        accuracy (float | None): The accuracy of the latitude and longitude. As an example, the accuracy can be
            measured in meters, such as the latitude and longitude are accurate to within 50 meters.
        altitude (float | None): The altitude of the location.
        altitudeAccuracy (float | None): The accuracy of the altitude.
        latitude (float | None): The latitude of the location.
        longitude (float | None): The longitude of the location.
    """

    accuracy: float | None = None
    altitude: float | None = None
    altitudeAccuracy: float | None = None
    latitude: float | None = None
    longitude: float | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.OutlookGeoCoordinates"
