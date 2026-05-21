from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from office365.runtime.client_value import ClientValue


@dataclass
class AuditSearchRequestStatus(ClientValue):
    CompletedTimeUtc: datetime | None = None
    CompletenessPercent: float | None = None
    CorrelationId: str | None = None
    CreatedTimeUtc: datetime | None = None
    DataGroupId: str | None = None
    ErrorMessage: str | None = None
    ExecutedTimeUtc: datetime | None = None
    JobId: str | None = None
    LastModifiedTimeUtc: datetime | None = None
    ProgressPercent: float | None = None
    Request: str | None = None
    RequestId: str | None = None
    RequestStorageName: str | None = None
    ResultStorageName: str | None = None
    SearchUser: str | None = None
    Status: int | None = None
    Throttled: bool | None = None
    TotalItemCount: int | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.AuditSearchRequestStatus"
