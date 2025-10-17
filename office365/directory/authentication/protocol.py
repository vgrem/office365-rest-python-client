from enum import Enum


class AuthenticationProtocol(Enum):
    wsFed = "0"
    saml = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AuthenticationProtocol"
