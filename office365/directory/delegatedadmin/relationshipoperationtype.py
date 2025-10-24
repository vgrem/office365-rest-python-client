from enum import Enum


class DelegatedAdminRelationshipOperationType(Enum):
    delegatedAdminAccessAssignmentUpdate = "0"
    unknownFutureValue = "1"
    delegatedAdminRelationshipUpdate = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.DelegatedAdminRelationshipOperationType"
