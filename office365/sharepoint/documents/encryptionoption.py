from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class EncryptionOption(ClientValue):
    AES256CBCKey: bytes | None = None
