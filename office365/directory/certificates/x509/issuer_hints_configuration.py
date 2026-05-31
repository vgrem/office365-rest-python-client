from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class X509CertificateIssuerHintsConfiguration(ClientValue):
    # state: X509CertificateIssuerHintsState = field(default_factory=X509CertificateIssuerHintsState)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.X509CertificateIssuerHintsConfiguration"
