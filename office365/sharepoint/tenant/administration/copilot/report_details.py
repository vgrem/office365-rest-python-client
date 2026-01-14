from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.tenant.administration.copilot.base_raw_data_sources import (
    BaseRawDataSources,
)
from office365.sharepoint.tenant.administration.copilot.reportrow import ReportRow


class ReportDetails(BaseRawDataSources):
    def __init__(
        self,
        headers: StringCollection = None,
        report_download_url: str = None,
        report_rows: ClientValueCollection[ReportRow] = ClientValueCollection(ReportRow),
    ):
        super().__init__()
        self.Headers = headers
        self.ReportDownloadUrl = report_download_url
        self.ReportRows = report_rows

    " "

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.TenantAdmin.Copilot.ReportDetails"
