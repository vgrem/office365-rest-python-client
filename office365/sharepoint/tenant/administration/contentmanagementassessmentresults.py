from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.sharepoint.tenant.administration.contentmanagementassessmentpolicyreportdetails import (
    ContentManagementAssessmentPolicyReportDetails as CMAPolicyDetails,
)
from office365.sharepoint.tenant.administration.reports.sitepermissionsdetails import (
    SitePermissionsReportDetails,
)


@dataclass
class ContentManagementAssessmentResults(ClientValue):
    lastUpdatedTime: datetime | None = None
    requestedTime: datetime | None = None
    siteLifecycleManagementImpactedFileUrl: str | None = None
    siteLifecycleManagementPolicyExecutionId: int | None = None
    siteLifecycleManagementPolicyId: str | None = None
    siteLifecycleManagementPolicyLastUpdatedTime: datetime | None = None
    siteLifecycleManagementPolicyResultState: int | None = None
    siteLifecycleManagementReportDetails: CMAPolicyDetails = field(default_factory=CMAPolicyDetails)
    sitePermissionsReportDefinitionId: str | None = None
    sitePermissionsReportDetails: SitePermissionsReportDetails = field(default_factory=SitePermissionsReportDetails)
    sitePermissionsReportId: str | None = None
    sitePermissionsReportLastUpdatedTime: datetime | None = None
    sitePermissionsReportQueuedTime: datetime | None = None
    sitePermissionsReportResultState: int | None = None
    totalCountOfSitesInTenant: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.ContentManagementAssessmentResults"
