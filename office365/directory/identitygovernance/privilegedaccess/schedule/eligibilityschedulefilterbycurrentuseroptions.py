from enum import Enum


class EligibilityScheduleFilterByCurrentUserOptions(Enum):
    principal = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.EligibilityScheduleFilterByCurrentUserOptions"
