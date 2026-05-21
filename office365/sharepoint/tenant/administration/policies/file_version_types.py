from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from office365.runtime.client_value import ClientValue


@dataclass
class SPOFileVersionBatchDeleteJobProgress(ClientValue):
    BatchDeleteMode: int | None = None
    CompleteTimeInUTC: datetime | None = None
    DeleteOlderThan: datetime | None = None
    ErrorMessage: str | None = None
    FilesProcessed: int | None = None
    FileTypeSelections: str | None = None
    LastProcessTimeInUTC: datetime | None = None
    ListsProcessed: int | None = None
    ListsSynced: int | None = None
    ListSyncFailed: int | None = None
    MajorVersionLimit: int | None = None
    MajorWithMinorVersionsLimit: int | None = None
    RequestTimeInUTC: datetime | None = None
    Status: str | None = None
    StorageReleasedInBytes: int | None = None
    SyncListPolicy: bool | None = None
    Url: str | None = None
    VersionsDeleted: int | None = None
    VersionsFailed: int | None = None
    VersionsProcessed: int | None = None
    WorkItemId: UUID | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOFileVersionBatchDeleteJobProgress"
