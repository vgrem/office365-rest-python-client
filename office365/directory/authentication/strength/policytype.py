from enum import Enum


class AuthenticationStrengthPolicyType(Enum):
    builtIn = "0"
    custom = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AuthenticationStrengthPolicyType"
