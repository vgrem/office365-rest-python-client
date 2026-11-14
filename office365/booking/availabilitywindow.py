from __future__ import annotations

from datetime import date

from office365.booking.availability import BookingsAvailability


class BookingsAvailabilityWindow(BookingsAvailability):
    endDate: date = date.min
    startDate: date = date.min

    @property
    def entity_type_name(self):
        return "microsoft.graph.BookingsAvailabilityWindow"
