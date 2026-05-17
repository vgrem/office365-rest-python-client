from enum import Enum


class AuthenticationMethodKeyStrength(Enum):
    normal = "0"
    weak = "1"
    unknown = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AuthenticationMethodKeyStrength"
