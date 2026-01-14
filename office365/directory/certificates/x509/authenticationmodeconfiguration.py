from office365.directory.certificates.x509.affinitylevel import X509CertificateAffinityLevel
from office365.directory.certificates.x509.authenticationmode import X509CertificateAuthenticationMode
from office365.directory.certificates.x509.rule import X509CertificateRule
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


class X509CertificateAuthenticationModeConfiguration(ClientValue):
    def __init__(
        self,
        rules: ClientValueCollection[X509CertificateRule] = ClientValueCollection(X509CertificateRule),
        authentication_default_mode: X509CertificateAuthenticationMode = X509CertificateAuthenticationMode.none,
        default_required_affinity_level: X509CertificateAffinityLevel = X509CertificateAffinityLevel.none,
        x509_certificate_authentication_default_mode: X509CertificateAuthenticationMode = (
            X509CertificateAuthenticationMode.none
        ),
        x509_certificate_default_required_affinity_level: X509CertificateAffinityLevel = (
            X509CertificateAffinityLevel.none,
        ),
    ):
        self.rules = rules
        self.x509CertificateAuthenticationDefaultMode = authentication_default_mode
        self.x509CertificateDefaultRequiredAffinityLevel = default_required_affinity_level
        self.x509CertificateAuthenticationDefaultMode = x509_certificate_authentication_default_mode
        self.x509CertificateDefaultRequiredAffinityLevel = x509_certificate_default_required_affinity_level

    @property
    def entity_type_name(self):
        return "microsoft.graph.X509CertificateAuthenticationModeConfiguration"
