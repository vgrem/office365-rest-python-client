from enum import Enum


class EligibilityScheduleRequestFilterByCurrentUserOptions(Enum):
    principal = "1"
    createdBy = "2"
    approver = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.EligibilityScheduleRequestFilterByCurrentUserOptions"
