from enum import Enum


class X509CertificateAffinityLevel(Enum):
    low = "0"
    high = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.X509CertificateAffinityLevel"
