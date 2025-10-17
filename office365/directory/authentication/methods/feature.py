from enum import Enum


class AuthenticationMethodFeature(Enum):
    ssprRegistered = "0"
    ssprEnabled = "1"
    ssprCapable = "2"
    passwordlessCapable = "3"
    mfaCapable = "4"
    unknownFutureValue = "5"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AuthenticationMethodFeature"
