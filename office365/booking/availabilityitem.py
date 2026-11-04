from __future__ import annotations

from dataclasses import field

from office365.booking.savailabilitystatus import BookingsAvailabilityStatus
from office365.outlook.calendar.dateTimeTimeZone import DateTimeTimeZone
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class AvailabilityItem(ClientValue):
    endDateTime: DateTimeTimeZone = field(default_factory=DateTimeTimeZone)
    serviceId: str | None = None
    startDateTime: DateTimeTimeZone = field(default_factory=DateTimeTimeZone)
    status: BookingsAvailabilityStatus = BookingsAvailabilityStatus.none

    @property
    def entity_type_name(self):
        return "microsoft.graph.AvailabilityItem"
