from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ContentManagementAssessmentOperationResult(ClientValue):
    dataAccessGovernanceErrorMessage: str | None = None
    siteLifecycleManagementErrorMessage: str | None = None
    siteLifecycleManagementPolicyResultState: int | None = None
    sitePermissionsReportResultState: int | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.TenantAdmin.ContentManagementAssessmentOperationResult"
