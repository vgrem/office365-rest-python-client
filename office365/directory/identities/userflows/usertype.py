from enum import Enum


class UserType(Enum):
    member = "0"
    guest = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.UserType"
