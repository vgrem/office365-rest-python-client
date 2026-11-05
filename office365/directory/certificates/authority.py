from __future__ import annotations

from office365.runtime.client_value import ClientValue


class CertificateAuthority(ClientValue):
    """Represents a certificate authority."""

    certificate: str | None = None
    certificateRevocationListUrl: str | None = None
    isRootAuthority: str | None = None
    issuer: str | None = None
    issuerSki: str | None = None
    deltaCertificateRevocationListUrl: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CertificateAuthority"
