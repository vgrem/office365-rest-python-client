from enum import Enum


class CertificateAuthorityType(Enum):
    root = "0"
    intermediate = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.CertificateAuthorityType"
