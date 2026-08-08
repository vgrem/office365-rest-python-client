from enum import Enum


class BroadcastMeetingAudience(Enum):
    roleIsAttendee = "0"
    organization = "1"
    everyone = "2"
    unknownFutureValue = "3"
    ""

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.BroadcastMeetingAudience"
