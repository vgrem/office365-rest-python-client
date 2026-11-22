from __future__ import annotations

from uuid import UUID

from office365.runtime.client_value import ClientValue


class LastAccessDateReportSiteStatus(ClientValue):
    AttemptCount: int | None = None
    FailureReason: str | None = None
    SiteId: UUID | None = None
    Status: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.TenantAdministration.LastAccessDateReportSiteStatus"
