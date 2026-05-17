from enum import Enum


class UserPurpose(Enum):
    user = "1"
    linked = "2"
    shared = "3"
    room = "4"
    equipment = "5"
    others = "6"
    unknownFutureValue = "7"

    @property
    def entity_type_name(self):
        return "microsoft.graph.UserPurpose"
