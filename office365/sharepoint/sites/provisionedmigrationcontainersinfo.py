from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ProvisionedMigrationContainersInfo(ClientValue):
    DataContainerUri: str | None = None
    EncryptionKey: bytes | None = None
    MetadataContainerUri: str | None = None
