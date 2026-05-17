from enum import Enum


class WindowsStartMenuAppListVisibilityType(Enum):
    userDefined = "0"
    collapse = "1"
    remove = "2"
    disableSettingsApp = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.WindowsStartMenuAppListVisibilityType"
