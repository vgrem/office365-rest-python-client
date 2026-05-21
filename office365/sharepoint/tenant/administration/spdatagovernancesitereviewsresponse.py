from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from office365.runtime.client_value import ClientValue


@dataclass
class SPDataGovernanceSiteReviewsResponse(ClientValue):
    AdminComment: str | None = None
    ReportCreatedDateTime: datetime | None = None
    ReportEndDateTime: datetime | None = None
    ReportEntity: int | None = None
    ReviewCompletedDateTime: datetime | None = None
    ReviewerComment: str | None = None
    ReviewerEmail: str | None = None
    ReviewId: UUID | None = None
    ReviewInitiatedDateTime: datetime | None = None
    SiteId: UUID | None = None
    SiteName: str | None = None
    Status: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPDataGovernanceSiteReviewsResponse"
