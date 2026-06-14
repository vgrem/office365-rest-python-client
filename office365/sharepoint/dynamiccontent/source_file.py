from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.publishing.sharepointids import SharePointIds


class SourceFile(ClientValue):
    DriveId: str | None = None
    Id: str | None = None
    SharePointIds: SharePointIds = field(default_factory=SharePointIds)

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.DynamicContent.timerjob.SourceFile"
