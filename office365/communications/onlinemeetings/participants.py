from typing import List

from office365.communications.onlinemeetings.participant_info import (
    MeetingParticipantInfo,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


class MeetingParticipants(ClientValue):
    """Participants in a meeting."""

    def __init__(self, organizer=MeetingParticipantInfo(), attendees: List[MeetingParticipantInfo] = None):
        """
        :param MeetingParticipantInfo organizer:
        :param list[MeetingParticipantInfo] attendees:
        """
        super().__init__()
        self.organizer = organizer
        self.attendees = ClientValueCollection(MeetingParticipantInfo, attendees)
