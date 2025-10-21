from enum import Enum


class WindowsUserAccountControlSettings(Enum):
    userDefined = "0"
    alwaysNotify = "1"
    notifyOnAppChanges = "2"
    notifyOnAppChangesWithoutDimming = "3"
    neverNotify = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.WindowsUserAccountControlSettings"
