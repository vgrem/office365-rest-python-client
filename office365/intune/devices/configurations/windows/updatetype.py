from enum import Enum


class WindowsUpdateType(Enum):
    userDefined = "0"
    all = "1"
    businessReadyOnly = "2"
    windowsInsiderBuildFast = "3"
    windowsInsiderBuildSlow = "4"
    windowsInsiderBuildRelease = "5"

    @property
    def entity_type_name(self):
        return "microsoft.graph.WindowsUpdateType"
