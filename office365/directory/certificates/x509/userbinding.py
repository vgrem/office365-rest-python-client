from typing import Optional

from office365.directory.certificates.x509.affinitylevel import X509CertificateAffinityLevel
from office365.runtime.client_value import ClientValue


class X509CertificateUserBinding(ClientValue):
    def __init__(
        self,
        priority: Optional[int] = None,
        trust_affinity_level: X509CertificateAffinityLevel = X509CertificateAffinityLevel.none,
        user_property: Optional[str] = None,
        x509_certificate_field: Optional[str] = None,
    ):
        self.priority = priority
        self.trustAffinityLevel = trust_affinity_level
        self.userProperty = user_property
        self.x509CertificateField = x509_certificate_field

    @property
    def entity_type_name(self):
        return "microsoft.graph.X509CertificateUserBinding"
