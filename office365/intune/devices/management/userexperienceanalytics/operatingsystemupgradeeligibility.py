from enum import Enum


class OperatingSystemUpgradeEligibility(Enum):
    upgraded = "0"
    unknown = "1"
    notCapable = "2"
    capable = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.OperatingSystemUpgradeEligibility"
