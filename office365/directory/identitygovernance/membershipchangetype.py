from enum import Enum


class MembershipChangeType(Enum):
    add = "1"
    remove = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.identityGovernance.MembershipChangeType"
