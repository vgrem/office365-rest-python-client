from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class Pkcs12CertificateInformation(ClientValue):
    """Represents the public information of a Pkcs12 certificate.

    Args:
        thumbprint (str): The certificate thumbprint
        notAfter (long): The certificate's expiry. This value is a NumericDate as defined in RFC 7519
          (A JSON numeric value representing the number of seconds from 1970-01-01T00:00:00Z UTC until the
          specified UTC date/time, ignoring leap seconds.)
        notBefore (long): The certificate's issue time (not before). This value is a NumericDate as defined in RFC
          7519 (A JSON numeric value representing the number of seconds from 1970-01-01T00:00:00Z UTC until the
          specified UTC date/time, ignoring leap seconds.)
    """

    thumbprint: str | None = None
    isActive: bool | None = None
    notAfter: int | None = None
    notBefore: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Pkcs12CertificateInformation"
