from enum import Enum


class PrivilegedAccessGroupRelationships(Enum):
    owner = "1"
    member = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.PrivilegedAccessGroupRelationships"
