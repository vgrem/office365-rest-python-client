from office365.runtime.client_value import ClientValue
from office365.sharepoint.tenant.administration.transpilerresponse import (
    TranspilerResponse,
)


class CopilotTranspilerResponse(ClientValue):
    def __init__(
        self,
        data: TranspilerResponse = TranspilerResponse(),
        error_message: str = None,
        is_eligible: bool = None,
    ):
        self.data = data
        self.errorMessage = error_message
        self.isEligible = is_eligible

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.TenantAdmin.Copilot.CopilotTranspilerResponse"
