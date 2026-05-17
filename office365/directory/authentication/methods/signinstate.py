from enum import Enum


class AuthenticationMethodSignInState(Enum):
    notSupported = "0"
    notAllowedByPolicy = "1"
    notEnabled = "2"
    phoneNumberNotUnique = "3"
    ready = "4"
    notConfigured = "5"
    unknownFutureValue = "6"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AuthenticationMethodSignInState"
