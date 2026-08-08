from __future__ import annotations

from dataclasses import dataclass

from office365.directory.certificates.x509.issuer_hints_state import X509CertificateIssuerHintsState
from office365.runtime.client_value import ClientValue


@dataclass
class X509CertificateIssuerHintsConfiguration(ClientValue):
    state: X509CertificateIssuerHintsState = X509CertificateIssuerHintsState.disabled

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.X509CertificateIssuerHintsConfiguration"
