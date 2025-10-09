from office365.runtime.client_value import ClientValue


class ContentManagementAssessmentOperationResult(ClientValue):

    def __init__(
        self,
        data_access_governance_error_message: str = None,
        site_lifecycle_management_error_message: str = None,
    ):
        self.dataAccessGovernanceErrorMessage = data_access_governance_error_message
        self.siteLifecycleManagementErrorMessage = (
            site_lifecycle_management_error_message
        )

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.TenantAdmin.ContentManagementAssessmentOperationResult"
