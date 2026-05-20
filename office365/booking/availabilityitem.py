from __future__ import annotations

from dataclasses import dataclass, field

from office365.booking.savailabilitystatus import BookingsAvailabilityStatus
from office365.outlook.calendar.dateTimeTimeZone import DateTimeTimeZone
from office365.runtime.client_value import ClientValue


@dataclass
class AvailabilityItem(ClientValue):
    endDateTime: DateTimeTimeZone = field(default_factory=DateTimeTimeZone)
    serviceId: str | None = None
    startDateTime: DateTimeTimeZone = field(default_factory=DateTimeTimeZone)
    status: BookingsAvailabilityStatus = BookingsAvailabilityStatus.none

    @property
    def entity_type_name(self):
        return "microsoft.graph.AvailabilityItem"
