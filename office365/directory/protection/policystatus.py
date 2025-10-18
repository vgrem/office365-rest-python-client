from enum import Enum


class ProtectionPolicyStatus(Enum):
    inactive = "0"
    activeWithErrors = "1"
    updating = "2"
    active = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ProtectionPolicyStatus"
