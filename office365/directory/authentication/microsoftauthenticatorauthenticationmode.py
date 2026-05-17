from enum import Enum


class MicrosoftAuthenticatorAuthenticationMode(Enum):
    deviceBasedPush = "0"
    push = "1"
    any = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.MicrosoftAuthenticatorAuthenticationMode"
