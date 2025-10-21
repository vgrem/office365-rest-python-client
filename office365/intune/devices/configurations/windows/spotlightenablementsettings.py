from enum import Enum


class WindowsSpotlightEnablementSettings(Enum):
    notConfigured = "0"
    disabled = "1"
    enabled = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.WindowsSpotlightEnablementSettings"
