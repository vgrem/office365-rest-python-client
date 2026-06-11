from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class EncryptionOption(ClientValue):
    AES256CBCKey: bytes | None = None
