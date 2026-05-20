from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharing.sitesharingreportjobdata import (
    SiteSharingReportJobData,
)


@dataclass
class SiteSharingReportStatus(ClientValue):
    errorCode: int | None = None
    jobData: SiteSharingReportJobData = field(default_factory=SiteSharingReportJobData)
    message: str | None = None
    success: bool | None = None

    @property
    def entity_type_name(self):
        return "SP.Sharing.SiteSharingReportStatus"
