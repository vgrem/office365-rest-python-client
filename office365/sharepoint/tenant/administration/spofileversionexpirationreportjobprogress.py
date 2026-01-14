from office365.runtime.client_value import ClientValue


class SPOFileVersionExpirationReportJobProgress(ClientValue):
    def __init__(
        self,
        error_message: str = None,
        report_url: str = None,
        status: str = None,
        url: str = None,
    ):
        self.ErrorMessage = error_message
        self.ReportUrl = report_url
        self.Status = status
        self.Url = url

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SPOFileVersionExpirationReportJobProgress"
