from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class CopyMigrationInfo(ClientValue):
    EncryptionKey: str | None = None
    JobId: str | None = None
    JobQueueUri: str | None = None
    SourceListItemUniqueIds: list[str] | None = None
