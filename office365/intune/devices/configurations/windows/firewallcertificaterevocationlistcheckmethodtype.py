from enum import Enum


class FirewallCertificateRevocationListCheckMethodType(Enum):
    deviceDefault = "0"
    none = "1"
    attempt = "2"
    require = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.FirewallCertificateRevocationListCheckMethodType"
