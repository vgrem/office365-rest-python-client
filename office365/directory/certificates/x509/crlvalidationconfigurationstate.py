from enum import Enum


class X509CertificateCRLValidationConfigurationState(Enum):
    disabled = "0"
    enabled = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.X509CertificateCRLValidationConfigurationState"
