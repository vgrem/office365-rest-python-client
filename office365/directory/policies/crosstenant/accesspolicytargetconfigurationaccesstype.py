from enum import Enum


class CrossTenantAccessPolicyTargetConfigurationAccessType(Enum):
    allowed = "1"
    blocked = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.CrossTenantAccessPolicyTargetConfigurationAccessType"
