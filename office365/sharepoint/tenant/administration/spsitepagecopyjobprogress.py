from __future__ import annotations

from uuid import UUID

from office365.runtime.client_value import ClientValue


class SPSitePageCopyJobProgress(ClientValue):
    ErrorMessage: str | None = None
    JobState: str | None = None
    NewPageUrl: str | None = None
    SourcePageName: str | None = None
    StatusMessage: str | None = None
    WorkItemId: UUID | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPSitePageCopyJobProgress"
