from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SiteSharingReportJobData(ClientValue):
    folderUrl: str | None = None
    webUrl: str | None = None

    @property
    def entity_type_name(self):
        return "SP.Sharing.SiteSharingReportJobData"
