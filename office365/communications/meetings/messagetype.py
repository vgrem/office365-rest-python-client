from enum import Enum


class MeetingMessageType(Enum):
    none = "0"
    meetingRequest = "1"
    meetingCancelled = "2"
    meetingAccepted = "3"
    meetingTenativelyAccepted = "4"
    meetingDeclined = "5"

    @property
    def entity_type_name(self):
        return "microsoft.graph.MeetingMessageType"
