from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class EncryptionOption(ClientValue):
    aes256_cbc_key: Optional[bytes] = None
