from enum import Enum


class Win32LobAppReturnCodeType(Enum):
    failed = "0"
    success = "1"
    softReboot = "2"
    hardReboot = "3"
    retry = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.Win32LobAppReturnCodeType"
