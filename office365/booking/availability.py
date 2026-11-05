from __future__ import annotations

from dataclasses import field

from office365.booking.serviceavailabilitytype import BookingsServiceAvailabilityType
from office365.booking.work_hours import BookingWorkHours
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


class BookingsAvailability(ClientValue):
    availabilityType: BookingsServiceAvailabilityType = BookingsServiceAvailabilityType.none
    businessHours: ClientValueCollection[BookingWorkHours] = field(
        default_factory=lambda: ClientValueCollection(BookingWorkHours)
    )

    @property
    def entity_type_name(self):
        return "microsoft.graph.BookingsAvailability"
