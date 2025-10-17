from enum import Enum


class MeetingLiveShareOptions(Enum):
    enabled = "0"
    disabled = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.MeetingLiveShareOptions"
