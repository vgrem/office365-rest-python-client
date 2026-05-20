from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharing.sitesharingreportjobdata import (
    SiteSharingReportJobData,
)


@dataclass
class SiteSharingReportCapabilities(ClientValue):
    canCancelSharingReport: bool | None = None
    canCreateSharingReport: bool | None = None
    createSharingReportNotAllowedReason: str | None = None
    jobData: SiteSharingReportJobData = field(default_factory=SiteSharingReportJobData)
    stopSharingReportNotAllowedReason: str | None = None

    ""

    @property
    def entity_type_name(self):
        return "SP.Sharing.SiteSharingReportCapabilities"
