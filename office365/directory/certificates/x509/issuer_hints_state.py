from __future__ import annotations

from enum import Enum


class X509CertificateIssuerHintsState(Enum):
    disabled = "0"
    enabled = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.X509CertificateIssuerHintsState"
