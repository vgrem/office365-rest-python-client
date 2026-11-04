from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ContentManagementAssessmentPolicyReportDetails(ClientValue):
    totalImpactedSites: int | None = None
    totalInactiveSites: int | None = None
    totalOwnerlessSites: int | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.ContentManagementAssessmentPolicyReportDetails"
