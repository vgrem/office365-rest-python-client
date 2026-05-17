from enum import Enum


class CertificateStatus(Enum):
    notProvisioned = "0"
    provisioned = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.CertificateStatus"
