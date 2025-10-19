from enum import Enum


class Win32LobAutoUpdateSupersededAppsState(Enum):
    notConfigured = "0"
    enabled = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.Win32LobAutoUpdateSupersededAppsState"
