from enum import Enum


class DelegatedAdminRelationshipRequestStatus(Enum):
    created = "0"
    pending = "1"
    succeeded = "2"
    failed = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.DelegatedAdminRelationshipRequestStatus"
