from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class X509CertificateIssuerHintsConfiguration(ClientValue):
    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.X509CertificateIssuerHintsConfiguration"
