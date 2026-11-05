from __future__ import annotations

from office365.runtime.client_value import ClientValue


class ProvisionedTemporaryAzureContainerInfo(ClientValue):
    EncryptionKey: bytes | None = None
    Uri: str | None = None
