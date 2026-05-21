from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.sharepoint.tenant.administration.errorfacet import ErrorFacet


@dataclass
class SPDataGovernanceSARStartSiteReviewResponse(ClientValue):
    AdminComment: str | None = None
    Error: ErrorFacet = field(default_factory=ErrorFacet)
    ReportEntity: int | None = None
    ReviewId: UUID | None = None
    ReviewInitiatedDateTime: datetime | None = None
    SiteId: UUID | None = None
    SiteName: str | None = None
    Status: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPDataGovernanceSARStartSiteReviewResponse"
