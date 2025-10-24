from enum import Enum


class EligibilityFilteringEnabledEntities(Enum):
    none = "0"
    swapRequest = "1"
    offerShiftRequest = "2"
    unknownFutureValue = "4"
    timeOffReason = "8"

    @property
    def entity_type_name(self):
        return "microsoft.graph.EligibilityFilteringEnabledEntities"
