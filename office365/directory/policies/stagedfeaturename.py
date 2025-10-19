from enum import Enum


class StagedFeatureName(Enum):
    passthroughAuthentication = "0"
    seamlessSso = "1"
    passwordHashSync = "2"
    emailAsAlternateId = "3"
    unknownFutureValue = "4"
    certificateBasedAuthentication = "5"
    multiFactorAuthentication = "6"

    @property
    def entity_type_name(self):
        return "microsoft.graph.StagedFeatureName"
