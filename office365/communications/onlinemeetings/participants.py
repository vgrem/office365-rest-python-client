from __future__ import annotations

from dataclasses import dataclass, field

from office365.communications.onlinemeetings.participant_info import (
    MeetingParticipantInfo,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class MeetingParticipants(ClientValue):
    """Participants in a meeting."""

    organizer: MeetingParticipantInfo = field(default_factory=MeetingParticipantInfo)
    attendees: ClientValueCollection = field(default_factory=lambda: ClientValueCollection(MeetingParticipantInfo))
