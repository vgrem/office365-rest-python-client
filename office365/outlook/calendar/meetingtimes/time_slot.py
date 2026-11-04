from __future__ import annotations

from dataclasses import field

from office365.outlook.calendar.dateTimeTimeZone import DateTimeTimeZone
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class TimeSlot(ClientValue):
    """Represents a time slot for a meeting.

    Fields:
        start (DateTimeTimeZone): The date, time, and time zone that a period begins.
        end (DateTimeTimeZone): The date, time, and time zone that a period ends.
    """

    end: DateTimeTimeZone = field(default_factory=DateTimeTimeZone)
    start: DateTimeTimeZone = field(default_factory=DateTimeTimeZone)

    def __repr__(self):
        return f"({self.start} - {self.end})"

    @property
    def entity_type_name(self):
        return "microsoft.graph.TimeSlot"
