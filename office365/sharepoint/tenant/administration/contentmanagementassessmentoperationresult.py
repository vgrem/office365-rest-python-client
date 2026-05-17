from office365.runtime.client_value import ClientValue
from typing import Optional


class ContentManagementAssessmentOperationResult(ClientValue):
    def __init__(
        self,
        data_access_governance_error_message: Optional[str] = None,
        site_lifecycle_management_error_message: Optional[str] = None,
    ):
        self.dataAccessGovernanceErrorMessage = data_access_governance_error_message
        self.siteLifecycleManagementErrorMessage = site_lifecycle_management_error_message

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.ContentManagementAssessmentOperationResult"
