from enum import Enum


class AuthenticationMethodTargetType(Enum):
    user = "0"
    group = "1"
    unknownFutureValue = "2"

    none = "-1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AuthenticationMethodTargetType"
