from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.sharepoint.sharing.sitesharingreportjobdata import (
    SiteSharingReportJobData,
)


@value
class SiteSharingReportStatus(ClientValue):
    errorCode: int | None = None
    jobData: SiteSharingReportJobData = field(default_factory=SiteSharingReportJobData)
    message: str | None = None
    success: bool | None = None

    @property
    def entity_type_name(self):
        return "SP.Sharing.SiteSharingReportStatus"
