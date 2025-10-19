from enum import Enum


class CloudPcRestorePointFrequencyType(Enum):
    default = "0"
    fourHours = "1"
    sixHours = "2"
    twelveHours = "3"
    sixteenHours = "4"
    twentyFourHours = "5"
    unknownFutureValue = "6"

    @property
    def entity_type_name(self):
        return "microsoft.graph.CloudPcRestorePointFrequencyType"
