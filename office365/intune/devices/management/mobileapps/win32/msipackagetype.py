from enum import Enum


class Win32LobAppMsiPackageType(Enum):
    perMachine = "0"
    perUser = "1"
    dualPurpose = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.Win32LobAppMsiPackageType"
