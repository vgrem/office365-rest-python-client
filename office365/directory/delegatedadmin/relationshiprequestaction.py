from enum import Enum


class DelegatedAdminRelationshipRequestAction(Enum):
    lockForApproval = "0"
    approve = "1"
    terminate = "2"
    unknownFutureValue = "3"
    reject = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.DelegatedAdminRelationshipRequestAction"
