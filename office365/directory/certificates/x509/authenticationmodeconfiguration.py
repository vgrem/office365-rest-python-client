from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.certificates.x509.affinitylevel import X509CertificateAffinityLevel
from office365.directory.certificates.x509.authenticationmode import X509CertificateAuthenticationMode
from office365.directory.certificates.x509.rule import X509CertificateRule
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class X509CertificateAuthenticationModeConfiguration(ClientValue):
    rules: ClientValueCollection[X509CertificateRule] = field(
        default_factory=lambda: ClientValueCollection(X509CertificateRule)
    )
    x509CertificateAuthenticationDefaultMode: X509CertificateAuthenticationMode = X509CertificateAuthenticationMode.none
    x509CertificateDefaultRequiredAffinityLevel: X509CertificateAffinityLevel = X509CertificateAffinityLevel.none

    @property
    def entity_type_name(self):
        return "microsoft.graph.X509CertificateAuthenticationModeConfiguration"
