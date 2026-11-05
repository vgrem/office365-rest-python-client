from __future__ import annotations

from office365.runtime.client_value import ClientValue


class SiteSharingReportJobData(ClientValue):
    folderUrl: str | None = None
    webUrl: str | None = None

    @property
    def entity_type_name(self):
        return "SP.Sharing.SiteSharingReportJobData"
