from __future__ import annotations

from office365.runtime.client_value import ClientValue


class ProvisionedMigrationContainersInfo(ClientValue):
    DataContainerUri: str | None = None
    EncryptionKey: bytes | None = None
    MetadataContainerUri: str | None = None
