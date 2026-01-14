from office365.runtime.client_value import ClientValue


class ReportMetadata(ClientValue):
    def __init__(self, report_metadata_details: dict = None):
        self.ReportMetadataDetails = report_metadata_details

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.TenantAdmin.Copilot.ReportMetadata"
