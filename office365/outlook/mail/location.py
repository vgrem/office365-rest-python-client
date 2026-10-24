from __future__ import annotations

from dataclasses import dataclass, field

from office365.outlook.geo_coordinates import OutlookGeoCoordinates
from office365.outlook.mail.physical_address import PhysicalAddress
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import Compare, odata


@dataclass
class Location(ClientValue):
    """
    Represents location information of an event.

    There are multiple ways to create events in a calendar, for example, through an app using the create event REST API,
    or manually using the Outlook user interface. When you create an event using the user interface, you can specify
    the location as plain text (for example, "Harry's Bar"), or from the rooms list provided by Outlook,
    Bing Autosuggest, or Bing local search.
    """

    #: What the sender names is the display name; the service resolves the rest of the location.
    address: PhysicalAddress = field(
        default_factory=PhysicalAddress, metadata=odata("address", compare=Compare(ignore=True))
    )
    coordinates: ClientValueCollection = field(
        default_factory=lambda: ClientValueCollection(OutlookGeoCoordinates),
        metadata=odata("coordinates", compare=Compare(ignore=True)),
    )
    displayName: str | None = None
    locationEmailAddress: str | None = field(
        default=None, metadata=odata("locationEmailAddress", compare=Compare(ignore=True))
    )
    locationType: str | None = field(default=None, metadata=odata("locationType", compare=Compare(ignore=True)))
    locationUri: str | None = field(default=None, metadata=odata("locationUri", compare=Compare(ignore=True)))
    uniqueId: str | None = field(default=None, metadata=odata("uniqueId", compare=Compare(ignore=True)))
    uniqueIdType: str | None = field(default=None, metadata=odata("uniqueIdType", compare=Compare(ignore=True)))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Location"
