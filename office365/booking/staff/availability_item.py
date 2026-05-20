from __future__ import annotations

from dataclasses import dataclass, field

from office365.booking.availabilityitem import AvailabilityItem
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class StaffAvailabilityItem(ClientValue):
    "Represents the available and busy time slots of a Microsoft Bookings staff member."

    availabilityItems: ClientValueCollection[AvailabilityItem] = field(
        default_factory=lambda: ClientValueCollection(AvailabilityItem)
    )
    staffId: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.StaffAvailabilityItem"
