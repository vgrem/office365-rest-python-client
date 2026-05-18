from __future__ import annotations

from dataclasses import dataclass, field

from office365.outlook.calendar.attendees.base import AttendeeBase
from office365.runtime.client_value import ClientValue


@dataclass
class AttendeeAvailability(ClientValue):
    """The availability of an attendees.

    Fields:
        attendee (AttendeeBase): The email address and type of attendee - whether it's a person or a resource,
            and whether required or optional if it's a person.
        availability (str | None): The availability status of the attendee.
    """

    attendee: AttendeeBase = field(default_factory=AttendeeBase)
    availability: str | None = None
