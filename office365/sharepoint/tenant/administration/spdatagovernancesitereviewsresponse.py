from datetime import datetime
from uuid import UUID

from office365.runtime.client_value import ClientValue
from typing import Optional


class SPDataGovernanceSiteReviewsResponse(ClientValue):
    def __init__(
        self,
        admin_comment: Optional[str] = None,
        report_created_date_time: Optional[datetime] = None,
        report_end_date_time: Optional[datetime] = None,
        report_entity: Optional[int] = None,
        review_completed_date_time: Optional[datetime] = None,
        reviewer_comment: Optional[str] = None,
        reviewer_email: Optional[str] = None,
        review_id: Optional[UUID] = None,
        review_initiated_date_time: Optional[datetime] = None,
        site_id: Optional[UUID] = None,
        site_name: Optional[str] = None,
        status: Optional[str] = None,
    ):
        self.AdminComment = admin_comment
        self.ReportCreatedDateTime = report_created_date_time
        self.ReportEndDateTime = report_end_date_time
        self.ReportEntity = report_entity
        self.ReviewCompletedDateTime = review_completed_date_time
        self.ReviewerComment = reviewer_comment
        self.ReviewerEmail = reviewer_email
        self.ReviewId = review_id
        self.ReviewInitiatedDateTime = review_initiated_date_time
        self.SiteId = site_id
        self.SiteName = site_name
        self.Status = status

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPDataGovernanceSiteReviewsResponse"
