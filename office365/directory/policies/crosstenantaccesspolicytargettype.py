from enum import Enum


class CrossTenantAccessPolicyTargetType(Enum):
    user = "1"
    group = "2"
    application = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.CrossTenantAccessPolicyTargetType"
