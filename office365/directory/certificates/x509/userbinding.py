from office365.directory.certificates.x509.affinitylevel import X509CertificateAffinityLevel
from office365.runtime.client_value import ClientValue


class X509CertificateUserBinding(ClientValue):
    def __init__(
        self,
        priority: int = None,
        trust_affinity_level: X509CertificateAffinityLevel = X509CertificateAffinityLevel.none,
        user_property: str = None,
        x509_certificate_field: str = None,
    ):
        self.priority = priority
        self.trustAffinityLevel = trust_affinity_level
        self.userProperty = user_property
        self.x509CertificateField = x509_certificate_field

    @property
    def entity_type_name(self):
        return "microsoft.graph.X509CertificateUserBinding"
