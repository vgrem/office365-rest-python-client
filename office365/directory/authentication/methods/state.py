from enum import Enum


class AuthenticationMethodState(Enum):
    enabled = "0"
    disabled = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AuthenticationMethodState"
