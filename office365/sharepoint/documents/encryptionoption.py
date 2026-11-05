from __future__ import annotations

from office365.runtime.client_value import ClientValue


class EncryptionOption(ClientValue):
    AES256CBCKey: bytes | None = None
