from __future__ import annotations

from dataclasses import dataclass, field

from office365.outlook.calendar.attendees.availability import AttendeeAvailability
from office365.outlook.calendar.meetingtimes.time_slot import TimeSlot
from office365.outlook.mail.location import Location
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class MeetingTimeSuggestion(ClientValue):
    """
    A meeting suggestion that includes information like meeting time, attendance likelihood, individual availability,
    and available meeting locations.
    """

    attendeeAvailability: ClientValueCollection = field(
        default_factory=lambda: ClientValueCollection(AttendeeAvailability)
    )
    confidence: float | None = None
    locations: ClientValueCollection = field(default_factory=lambda: ClientValueCollection(Location))
    meetingTimeSlot: TimeSlot = field(default_factory=TimeSlot)

    def __repr__(self):
        return repr(self.meetingTimeSlot)
