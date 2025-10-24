from enum import Enum


class TeamworkCallEventType(Enum):
    call = "0"
    meeting = "1"
    screenShare = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.TeamworkCallEventType"
