from __future__ import annotations

from dataclasses import field
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.tenantadministration.last_access_date_report_site_in_progress import (
    LastAccessDateReportSiteInProgress,
)


class LastAccessDateReportStartResult(ClientValue):
    QueuedSiteCount: int | None = None
    RunId: UUID | None = None
    SitesAlreadyInProgress: ClientValueCollection[LastAccessDateReportSiteInProgress] = field(
        default_factory=lambda: ClientValueCollection(LastAccessDateReportSiteInProgress)
    )

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.TenantAdministration.LastAccessDateReportStartResult"
