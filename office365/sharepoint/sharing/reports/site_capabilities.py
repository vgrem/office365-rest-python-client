from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharing.sitesharingreportjobdata import (
    SiteSharingReportJobData,
)


class SiteSharingReportCapabilities(ClientValue):

    def __init__(
        self,
        can_cancel_sharing_report: bool = None,
        can_create_sharing_report: bool = None,
        create_sharing_report_not_allowed_reason: str = None,
        job_data: SiteSharingReportJobData = SiteSharingReportJobData(),
        stop_sharing_report_not_allowed_reason: str = None,
    ):
        self.canCancelSharingReport = can_cancel_sharing_report
        self.canCreateSharingReport = can_create_sharing_report
        self.createSharingReportNotAllowedReason = create_sharing_report_not_allowed_reason
        self.jobData = job_data
        self.stopSharingReportNotAllowedReason = stop_sharing_report_not_allowed_reason

    ""

    @property
    def entity_type_name(self):
        return "SP.Sharing.SiteSharingReportCapabilities"
