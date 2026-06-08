from __future__ import annotations

from dataclasses import dataclass, field

from office365.onedrive.driveitems.geo_coordinates import GeoCoordinates
from office365.runtime.client_value import ClientValue


@dataclass
class SignInLocation(ClientValue):
    """Provides the city, state and country/region from where the sign-in happened.

    Args:
        city (str): Provides the city where the sign-in originated. This is calculated using latitude/longitude
          information from the sign-in activity.
        countryOrRegion (str): Provides the country code info (2 letter code) where the sign-in originated.
          This is calculated using latitude/longitude information from the sign-in activity.
        geoCoordinates (GeoCoordinates): Provides the latitude, longitude and altitude where the sign-in originated.
        state (str): Provides the State where the sign-in originated. This is calculated using latitude/longitude
          information from the sign-in activity.
    """

    city: str | None = None
    countryOrRegion: str | None = None
    geoCoordinates: GeoCoordinates = field(default_factory=GeoCoordinates)
    state: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.SignInLocation"
