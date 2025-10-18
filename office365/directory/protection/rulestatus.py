from enum import Enum


class ProtectionRuleStatus(Enum):
    draft = "0"
    active = "1"
    completed = "2"
    completedWithErrors = "3"
    unknownFutureValue = "4"
    updateRequested = "5"
    deleteRequested = "6"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ProtectionRuleStatus"
