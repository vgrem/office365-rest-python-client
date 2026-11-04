from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ProvisionedMigrationContainersInfo(ClientValue):
    DataContainerUri: str | None = None
    EncryptionKey: bytes | None = None
    MetadataContainerUri: str | None = None
