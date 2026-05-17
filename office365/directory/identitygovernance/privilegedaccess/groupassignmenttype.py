from enum import Enum


class PrivilegedAccessGroupAssignmentType(Enum):
    assigned = "1"
    activated = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.PrivilegedAccessGroupAssignmentType"
