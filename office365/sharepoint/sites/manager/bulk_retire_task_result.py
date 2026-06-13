from __future__ import annotations

from office365.runtime.client_value import ClientValue


class BulkRetireTaskResult(ClientValue):
    PagePath: str | None = None
    PageTitle: str | None = None
    PendingChangesDiscarded: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.SiteManager.BulkRetireTaskResult"
