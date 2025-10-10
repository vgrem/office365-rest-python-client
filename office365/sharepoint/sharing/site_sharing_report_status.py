from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharing.sitesharingreportjobdata import (
    SiteSharingReportJobData,
)


class SiteSharingReportStatus(ClientValue):

    def __init__(
        self,
        error_code: int = None,
        job_data: SiteSharingReportJobData = SiteSharingReportJobData(),
        message: str = None,
        success: bool = None,
    ):
        self.errorCode = error_code
        self.jobData = job_data
        self.message = message
        self.success = success

    @property
    def entity_type_name(self):
        return "SP.Sharing.SiteSharingReportStatus"
