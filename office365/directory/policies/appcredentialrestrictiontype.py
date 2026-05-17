from enum import Enum


class AppCredentialRestrictionType(Enum):
    passwordAddition = "0"
    passwordLifetime = "1"
    symmetricKeyAddition = "2"
    symmetricKeyLifetime = "3"
    customPasswordAddition = "4"
    unknownFutureValue = "99"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AppCredentialRestrictionType"
