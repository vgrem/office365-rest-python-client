from __future__ import annotations

from datetime import datetime
from uuid import UUID

from office365.runtime.client_value import ClientValue


class LastAccessDateReportRequestSummary(ClientValue):
    Completed: int | None = None
    Failed: int | None = None
    InProgress: int | None = None
    Mode: int | None = None
    NotStarted: int | None = None
    PackageState: int | None = None
    PackageUrl: str | None = None
    RequestedUtc: datetime | None = None
    Retrying: int | None = None
    RunId: UUID | None = None
    TotalSites: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.TenantAdministration.LastAccessDateReportRequestSummary"
