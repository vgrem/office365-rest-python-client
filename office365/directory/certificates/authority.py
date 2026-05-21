from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class CertificateAuthority(ClientValue):
    """Represents a certificate authority."""

    certificate: str | None = None
    certificateRevocationListUrl: str | None = None
    isRootAuthority: str | None = None
    issuer: str | None = None
    issuerSki: str | None = None
