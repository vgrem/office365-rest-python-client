from enum import Enum


class Win32LobAppDeliveryOptimizationPriority(Enum):
    notConfigured = "0"
    foreground = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.Win32LobAppDeliveryOptimizationPriority"
