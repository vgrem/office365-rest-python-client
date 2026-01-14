from office365.directory.certificates.x509.affinitylevel import X509CertificateAffinityLevel
from office365.directory.certificates.x509.authenticationmode import X509CertificateAuthenticationMode
from office365.directory.certificates.x509.ruletype import X509CertificateRuleType
from office365.runtime.client_value import ClientValue


class X509CertificateRule(ClientValue):
    def __init__(
        self,
        identifier: str = None,
        issuer_subject_identifier: str = None,
        policy_oid_identifier: str = None,
        x509_certificate_authentication_mode: X509CertificateAuthenticationMode = X509CertificateAuthenticationMode.none,
        x509_certificate_required_affinity_level: X509CertificateAffinityLevel = X509CertificateAffinityLevel.none,
        x509_certificate_rule_type: X509CertificateRuleType = X509CertificateRuleType.none,
    ):
        self.identifier = identifier
        self.issuerSubjectIdentifier = issuer_subject_identifier
        self.policyOidIdentifier = policy_oid_identifier
        self.x509CertificateAuthenticationMode = x509_certificate_authentication_mode
        self.x509CertificateRequiredAffinityLevel = x509_certificate_required_affinity_level
        self.x509CertificateRuleType = x509_certificate_rule_type

    @property
    def entity_type_name(self):
        return "microsoft.graph.X509CertificateRule"
