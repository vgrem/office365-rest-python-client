from enum import Enum


class MeetingChatMode(Enum):
    enabled = "0"
    disabled = "1"
    limited = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.MeetingChatMode"
