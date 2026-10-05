"""Helpers for X.509 client-certificate authentication.

Entra stores a certificate's SHA-1 thumbprint (upper-case hex) in
``keyCredential.customKeyIdentifier``; MSAL expects that thumbprint for legacy
certificate authentication, or a PEM public certificate for subject name/issuer
(SNI) authentication. These helpers normalise the supported certificate inputs
(DER/PEM bytes, inline PEM text, or a file path) and build the MSAL
``client_credential`` dictionary.
"""

from __future__ import annotations

import hashlib
import os
import ssl
from pathlib import Path
from typing import Any, Dict, Union

from typing_extensions import TypeAlias

#: Certificate material: raw DER/PEM bytes, inline PEM text, or a file path.
CertificateData: TypeAlias = Union[bytes, bytearray, str, "os.PathLike[str]"]


def read_certificate(cert_data: CertificateData) -> bytes:
    """Return the raw certificate bytes.

    Accepts DER/PEM bytes, inline PEM text, or a path to a certificate file.
    """
    if isinstance(cert_data, (bytes, bytearray)):
        return bytes(cert_data)
    if isinstance(cert_data, str) and "-----BEGIN" in cert_data:
        return cert_data.encode("utf-8")
    return Path(cert_data).read_bytes()


def certificate_der(cert_data: CertificateData) -> bytes:
    """Normalise a certificate to DER, as Entra expects for ``keyCredentials.key``."""
    raw = read_certificate(cert_data)
    if raw.lstrip().startswith(b"-----BEGIN"):
        return ssl.PEM_cert_to_DER_cert(raw.decode("ascii"))
    return raw


def certificate_pem(cert_data: CertificateData) -> str:
    """Return the certificate as PEM text (MSAL sends this in the SNI ``x5c`` header)."""
    raw = read_certificate(cert_data)
    if raw.lstrip().startswith(b"-----BEGIN"):
        return raw.decode("ascii")
    return ssl.DER_cert_to_PEM_cert(raw)


def certificate_thumbprint(cert_data: CertificateData) -> str:
    """Compute the SHA-1 thumbprint in the upper-case hex form Entra uses.

    Entra stores this value in ``keyCredential.customKeyIdentifier``.
    """
    return hashlib.sha1(certificate_der(cert_data)).hexdigest().upper()


def build_client_credential(
    *,
    thumbprint: str | None = None,
    private_key: str | None = None,
    public_certificate: CertificateData | None = None,
    passphrase: str | None = None,
    use_sni: bool = False,
) -> Dict[str, Any]:
    """Build the MSAL ``client_credential`` dictionary for a client certificate.

    Args:
        thumbprint: Hex encoded SHA-1 thumbprint. When omitted, it is derived
            from ``public_certificate``.
        private_key: PEM encoded private key.
        public_certificate: Certificate (DER/PEM bytes, inline PEM text, or a
            file path), used to derive the thumbprint or, with ``use_sni``, sent
            to Entra in the ``x5c`` header.
        passphrase: Private key passphrase.
        use_sni: Use subject name/issuer authentication (PS256 + ``x5c``) instead
            of the legacy SHA-1 thumbprint. Requires the optional
            ``cryptography`` package and a certificate issued by a trusted CA.

    Raises:
        ValueError: If neither ``thumbprint`` nor ``public_certificate`` is provided.
        ImportError: If ``use_sni`` is requested without ``cryptography`` installed.
    """
    credentials: Dict[str, Any] = {"private_key": private_key}
    if thumbprint:
        credentials["thumbprint"] = thumbprint
    elif public_certificate is None:
        raise ValueError("Provide either 'thumbprint' or 'public_certificate' for certificate authentication")
    elif use_sni:
        try:
            import cryptography  # noqa: F401
        except ImportError as exc:
            raise ImportError(
                "SNI certificate authentication requires the optional 'cryptography' package; "
                "install it or pass a 'thumbprint' instead."
            ) from exc
        credentials["public_certificate"] = certificate_pem(public_certificate)
    else:
        credentials["thumbprint"] = certificate_thumbprint(public_certificate)
    if passphrase:
        credentials["passphrase"] = passphrase
    return credentials
