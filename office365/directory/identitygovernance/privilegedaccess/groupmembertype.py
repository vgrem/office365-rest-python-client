from enum import Enum


class PrivilegedAccessGroupMemberType(Enum):
    direct = "1"
    group = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.PrivilegedAccessGroupMemberType"
