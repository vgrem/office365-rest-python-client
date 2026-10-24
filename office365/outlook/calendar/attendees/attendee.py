from __future__ import annotations

from dataclasses import dataclass, field

from office365.outlook.calendar.attendees.base import AttendeeBase
from office365.outlook.calendar.meetingtimes.time_slot import TimeSlot
from office365.outlook.calendar.response_status import ResponseStatus
from office365.runtime.types.odata_property import Compare, odata


@dataclass
class Attendee(AttendeeBase):
    """An event attendees. This can be a person or resource such as a meeting room or equipment,
    that has been set up as a resource on the Exchange server for the tenant."""

    #: What the attendee answered, not what the sender asked: not part of the invitation.
    proposedNewTime: TimeSlot | None = field(
        default=None, metadata=odata("proposedNewTime", compare=Compare(ignore=True))
    )
    status: ResponseStatus | None = field(default=None, metadata=odata("status", compare=Compare(ignore=True)))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Attendee"
