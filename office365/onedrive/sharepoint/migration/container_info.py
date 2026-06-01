from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SharePointMigrationContainerInfo(ClientValue):
    dataContainerUri: str | None = None
    encryptionKey: str | None = None
    metadataContainerUri: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SharePointMigrationContainerInfo"
