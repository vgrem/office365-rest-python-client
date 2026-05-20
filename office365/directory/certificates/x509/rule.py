from __future__ import annotations

from dataclasses import dataclass

from office365.directory.certificates.x509.affinitylevel import X509CertificateAffinityLevel
from office365.directory.certificates.x509.authenticationmode import X509CertificateAuthenticationMode
from office365.directory.certificates.x509.ruletype import X509CertificateRuleType
from office365.runtime.client_value import ClientValue


@dataclass
class X509CertificateRule(ClientValue):
    identifier: str | None = None
    issuerSubjectIdentifier: str | None = None
    policyOidIdentifier: str | None = None
    x509CertificateAuthenticationMode: X509CertificateAuthenticationMode = X509CertificateAuthenticationMode.none
    x509CertificateRequiredAffinityLevel: X509CertificateAffinityLevel = X509CertificateAffinityLevel.none
    x509CertificateRuleType: X509CertificateRuleType = X509CertificateRuleType.none

    @property
    def entity_type_name(self):
        return "microsoft.graph.X509CertificateRule"
