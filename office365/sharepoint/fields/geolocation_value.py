from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class FieldGeolocationValue(ClientValue):
    """
    Specifies altitude, latitude, longitude and measure values for FieldGeolocation (section 3.2.5.185).<191>

    Fields:
        Latitude (float): Specifies the latitude value for Geolocation field.
        Longitude (float): Specifies the longitude value for Geolocation field.
        Altitude (float | None): Specifies the altitude value for Geolocation field. It is a user defined value
        Measure (float | None):
    """

    Latitude: float
    Longitude: float
    Altitude: float | None = None
    Measure: float | None = None

    @property
    def entity_type_name(self):
        return "SP.FieldGeolocationValue"
