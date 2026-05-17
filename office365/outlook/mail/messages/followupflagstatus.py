from enum import Enum


class FollowupFlagStatus(Enum):
    notFlagged = "0"
    complete = "1"
    flagged = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.FollowupFlagStatus"
