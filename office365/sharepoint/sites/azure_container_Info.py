from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ProvisionedTemporaryAzureContainerInfo(ClientValue):
    EncryptionKey: bytes | None = None
    Uri: str | None = None
