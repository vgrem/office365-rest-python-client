from enum import Enum


class B2bIdentityProvidersType(Enum):
    azureActiveDirectory = "1"
    externalFederation = "2"
    socialIdentityProviders = "3"
    emailOneTimePasscode = "4"
    microsoftAccount = "5"
    defaultConfiguredIdp = "6"
    unknownFutureValue = "7"

    @property
    def entity_type_name(self):
        return "microsoft.graph.B2bIdentityProvidersType"
