from uuid import UUID

from office365.runtime.client_value import ClientValue


class SPDataGovernanceInsightMetadata(ClientValue):

    def __init__(self, report_id: UUID = None, status: str = None):
        self.ReportId = report_id
        self.Status = status

    " "

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPDataGovernanceInsightMetadata"
