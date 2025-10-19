from enum import Enum


class SiteLockState(Enum):
    unlocked = "0"
    lockedReadOnly = "1"
    lockedNoAccess = "2"
    lockedNoAdditions = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.SiteLockState"
