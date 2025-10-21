from enum import Enum


class InstallState(Enum):
    notApplicable = "0"
    installed = "1"
    failed = "2"
    notInstalled = "3"
    uninstallFailed = "4"
    unknown = "5"

    @property
    def entity_type_name(self):
        return "microsoft.graph.InstallState"
