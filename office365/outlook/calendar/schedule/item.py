from __future__ import annotations

from dataclasses import dataclass, field

from office365.outlook.calendar.dateTimeTimeZone import DateTimeTimeZone
from office365.runtime.client_value import ClientValue


@dataclass
class ScheduleItem(ClientValue):
    """
    An item that describes the availability of a user corresponding to an actual event on the user's default calendar.
    This item applies to a resource (room or equipment) as well.

    Fields:
        start (DateTimeTimeZone): The date, time, and time zone that the corresponding event starts.
        end (DateTimeTimeZone): The date, time, and time zone that the corresponding event ends.
        location (str | None): The location where the corresponding event is held or attended from. Optional.
        isPrivate (bool | None): The sensitivity of the corresponding event. True if the event is marked private,
            false otherwise. Optional.
        subject (str | None): The corresponding event's subject line. Optional.
        status (str | None): The availability status of the user or resource during the corresponding event.
            The possible values are: free, tentative, busy, oof, workingElsewhere, unknown.
    """

    end: DateTimeTimeZone = field(default_factory=DateTimeTimeZone)
    isPrivate: bool | None = None
    location: str | None = None
    start: DateTimeTimeZone = field(default_factory=DateTimeTimeZone)
    status: str | None = None
    subject: str | None = None
