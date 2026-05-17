from datetime import datetime
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.sharepoint.tenant.administration.errorfacet import ErrorFacet
from typing import Optional


class SPDataGovernanceSARStartSiteReviewResponse(ClientValue):
    def __init__(
        self,
        admin_comment: Optional[str] = None,
        error: ErrorFacet = ErrorFacet(),
        report_entity: Optional[int] = None,
        review_id: Optional[UUID] = None,
        review_initiated_date_time: Optional[datetime] = None,
        site_id: Optional[UUID] = None,
        site_name: Optional[str] = None,
        status: Optional[str] = None,
    ):
        self.AdminComment = admin_comment
        self.Error = error
        self.ReportEntity = report_entity
        self.ReviewId = review_id
        self.ReviewInitiatedDateTime = review_initiated_date_time
        self.SiteId = site_id
        self.SiteName = site_name
        self.Status = status

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPDataGovernanceSARStartSiteReviewResponse"
