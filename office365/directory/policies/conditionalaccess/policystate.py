from enum import Enum


class ConditionalAccessPolicyState(Enum):
    enabled = "0"
    disabled = "1"
    enabledForReportingButNotEnforced = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ConditionalAccessPolicyState"
