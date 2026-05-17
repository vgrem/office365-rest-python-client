from enum import Enum


class AuthenticationStrengthRequirements(Enum):
    none = "0"
    mfa = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AuthenticationStrengthRequirements"
