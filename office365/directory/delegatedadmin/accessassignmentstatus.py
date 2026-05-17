from enum import Enum


class DelegatedAdminAccessAssignmentStatus(Enum):
    pending = "0"
    active = "1"
    deleting = "2"
    deleted = "3"
    error = "4"
    unknownFutureValue = "5"

    @property
    def entity_type_name(self):
        return "microsoft.graph.DelegatedAdminAccessAssignmentStatus"
