from __future__ import annotations

from dataclasses import field
from datetime import timedelta

from office365.booking.availability import BookingsAvailability
from office365.booking.availabilitywindow import BookingsAvailabilityWindow
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


class BookingSchedulingPolicy(ClientValue):
    allowStaffSelection: bool | None = None
    customAvailabilities: ClientValueCollection[BookingsAvailabilityWindow] = field(
        default_factory=lambda: ClientValueCollection(BookingsAvailabilityWindow)
    )
    generalAvailability: BookingsAvailability | None = None
    isMeetingInviteToCustomersEnabled: bool | None = None
    maximumAdvance: timedelta | None = None
    minimumLeadTime: timedelta | None = None
    sendConfirmationsToOwner: bool | None = None
    timeSlotInterval: timedelta | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.BookingSchedulingPolicy"
