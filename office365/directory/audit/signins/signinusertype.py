from enum import Enum


class SignInUserType(Enum):
    member = "0"
    guest = "1"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.SignInUserType"
