from enum import Enum


class UnifiedRoleManagementPolicyRuleTargetOperations(Enum):
    all = "0"
    activate = "1"
    deactivate = "2"
    assign = "3"
    update = "4"
    remove = "5"
    extend = "6"
    renew = "7"
    unknownFutureValue = "8"

    @property
    def entity_type_name(self):
        return "microsoft.graph.UnifiedRoleManagementPolicyRuleTargetOperations"
