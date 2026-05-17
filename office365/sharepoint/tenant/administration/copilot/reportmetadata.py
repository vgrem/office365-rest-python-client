from office365.runtime.client_value import ClientValue
from typing import Optional


class ReportMetadata(ClientValue):
    def __init__(self, report_metadata_details: Optional[dict] = None):
        self.ReportMetadataDetails = report_metadata_details

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.Copilot.ReportMetadata"
