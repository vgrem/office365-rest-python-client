from __future__ import annotations

from office365.runtime.client_value import ClientValue


class DocumentsDataSource(ClientValue):
    documentFolderId: str | None = None
    documentLibraryId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.SiteManager.DocumentsDataSource"
