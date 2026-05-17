from enum import Enum


class DefenderCloudBlockLevelType(Enum):
    notConfigured = "0"
    high = "1"
    highPlus = "2"
    zeroTolerance = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.DefenderCloudBlockLevelType"
