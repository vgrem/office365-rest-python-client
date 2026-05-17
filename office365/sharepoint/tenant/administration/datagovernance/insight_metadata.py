from typing import Optional
from uuid import UUID

from office365.runtime.client_value import ClientValue


class SPDataGovernanceInsightMetadata(ClientValue):
    def __init__(self, report_id: Optional[UUID] = None, status: Optional[str] = None):
        self.ReportId = report_id
        self.Status = status

    " "

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPDataGovernanceInsightMetadata"
