from enum import Enum


class WindowsStartMenuModeType(Enum):
    userDefined = "0"
    fullScreen = "1"
    nonFullScreen = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.WindowsStartMenuModeType"
