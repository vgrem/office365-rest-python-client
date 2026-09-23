"""AES-256-CBC helpers for SharePoint Migration API packages.

SharePoint-provided migration containers require the content **and** manifest
blobs to be encrypted client-side with the AES256CBC key returned by
``Site.provision_migration_containers``. Each blob gets a unique random IV, stored
as its base64 ``IV`` blob property.

Requires the ``[azure]`` extra (``cryptography``).
"""

from __future__ import annotations

import base64
import os

__all__ = ["decrypt", "encrypt", "normalize_key"]

_HINT = "AES encryption requires the 'azure' extra: pip install office365-rest-python-client[azure]"

_BLOCK_SIZE = 128


def normalize_key(value: str | bytes) -> bytes:
    """The raw AES key — a base64 string is decoded, bytes are used as-is."""
    return base64.b64decode(value) if isinstance(value, str) else value


def encrypt(data: bytes, key: bytes) -> tuple[bytes, str]:
    """AES-256-CBC encrypt ``data``; returns ``(ciphertext, base64 IV)``."""
    Cipher, algorithms, modes, padding = _crypto()
    iv = os.urandom(algorithms.AES.block_size // 8)
    padder = padding.PKCS7(_BLOCK_SIZE).padder()
    padded = padder.update(data) + padder.finalize()
    encryptor = Cipher(algorithms.AES(key), modes.CBC(iv)).encryptor()
    return encryptor.update(padded) + encryptor.finalize(), base64.b64encode(iv).decode("ascii")


def decrypt(data: bytes, key: bytes, iv: str) -> bytes:
    """AES-256-CBC decrypt ``data`` given the base64 ``iv`` (used by tests)."""
    Cipher, algorithms, modes, padding = _crypto()
    decryptor = Cipher(algorithms.AES(key), modes.CBC(base64.b64decode(iv))).decryptor()
    padded = decryptor.update(data) + decryptor.finalize()
    unpadder = padding.PKCS7(_BLOCK_SIZE).unpadder()
    return unpadder.update(padded) + unpadder.finalize()


def _crypto():
    """Lazily import the ``cryptography`` primitives (optional extra)."""
    try:
        from cryptography.hazmat.primitives import padding
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    except ImportError as exc:  # pragma: no cover - exercised only without the extra
        raise ImportError(_HINT) from exc
    return Cipher, algorithms, modes, padding
