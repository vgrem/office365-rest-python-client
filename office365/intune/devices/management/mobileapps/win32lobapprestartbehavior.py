from enum import Enum


class Win32LobAppRestartBehavior(Enum):
    basedOnReturnCode = "0"
    allow = "1"
    suppress = "2"
    force = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.Win32LobAppRestartBehavior"
