from typing import Optional

from office365.runtime.client_value import ClientValue


class SPOFileVersionExpirationReportJobProgress(ClientValue):
    def __init__(
        self,
        error_message: Optional[str] = None,
        report_url: Optional[str] = None,
        status: Optional[str] = None,
        url: Optional[str] = None,
    ):
        self.ErrorMessage = error_message
        self.ReportUrl = report_url
        self.Status = status
        self.Url = url

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOFileVersionExpirationReportJobProgress"
