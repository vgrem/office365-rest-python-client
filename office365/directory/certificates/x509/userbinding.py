from __future__ import annotations

from dataclasses import dataclass

from office365.directory.certificates.x509.affinitylevel import X509CertificateAffinityLevel
from office365.runtime.client_value import ClientValue


@dataclass
class X509CertificateUserBinding(ClientValue):
    priority: int | None = None
    trustAffinityLevel: X509CertificateAffinityLevel = X509CertificateAffinityLevel.none
    userProperty: str | None = None
    x509CertificateField: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.X509CertificateUserBinding"
