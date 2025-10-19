from enum import Enum


class X509CertificateAuthenticationMode(Enum):
    x509CertificateSingleFactor = "0"
    x509CertificateMultiFactor = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.X509CertificateAuthenticationMode"
