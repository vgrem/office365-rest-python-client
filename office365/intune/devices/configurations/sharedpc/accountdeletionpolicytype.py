from enum import Enum


class SharedPCAccountDeletionPolicyType(Enum):
    immediate = "0"
    diskSpaceThreshold = "1"
    diskSpaceThresholdOrInactiveThreshold = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.SharedPCAccountDeletionPolicyType"
