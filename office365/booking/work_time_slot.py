from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class BookingWorkTimeSlot(ClientValue):
    """Defines the start and end times for work.

    Fields:
        endTime (str | None): The time of the day when work stops. For example, 17:00:00.0000000.
        startTime (str | None): The time of the day when work starts. For example, 08:00:00.0000000.
    """

    endTime: str | None = None
    startTime: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.BookingWorkTimeSlot"
