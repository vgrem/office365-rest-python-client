from enum import Enum


class IncludedUserRoles(Enum):
    all = "0"
    privilegedAdmin = "1"
    admin = "2"
    user = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.IncludedUserRoles"
