from enum import Enum


class Win32LobAppNotification(Enum):
    showAll = "0"
    showReboot = "1"
    hideAll = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.Win32LobAppNotification"
