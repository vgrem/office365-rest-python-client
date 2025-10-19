from enum import Enum


class TokenIssuerType(Enum):
    AzureAD = "0"
    ADFederationServices = "1"
    UnknownFutureValue = "2"
    AzureADBackupAuth = "3"
    ADFederationServicesMFAAdapter = "4"
    NPSExtension = "5"

    @property
    def entity_type_name(self):
        return "microsoft.graph.TokenIssuerType"
