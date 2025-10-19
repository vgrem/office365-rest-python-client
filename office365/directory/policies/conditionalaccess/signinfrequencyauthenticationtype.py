from enum import Enum


class SignInFrequencyAuthenticationType(Enum):
    primaryAndSecondaryAuthentication = "0"
    secondaryAuthentication = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.SignInFrequencyAuthenticationType"
