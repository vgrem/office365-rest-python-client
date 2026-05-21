from __future__ import annotations

from dataclasses import dataclass, field

from office365.outlook.geo_coordinates import OutlookGeoCoordinates
from office365.outlook.mail.physical_address import PhysicalAddress
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class Location(ClientValue):
    """
    Represents location information of an event.

    There are multiple ways to create events in a calendar, for example, through an app using the create event REST API,
    or manually using the Outlook user interface. When you create an event using the user interface, you can specify
    the location as plain text (for example, "Harry's Bar"), or from the rooms list provided by Outlook,
    Bing Autosuggest, or Bing local search.
    """

    address: PhysicalAddress = field(default_factory=PhysicalAddress)
    coordinates: ClientValueCollection = field(
        default_factory=lambda: ClientValueCollection(OutlookGeoCoordinates)
    )
    displayName: str | None = None
    locationEmailAddress: str | None = None
    locationType: str | None = None
    locationUri: str | None = None
    uniqueId: str | None = None
    uniqueIdType: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.Location"
