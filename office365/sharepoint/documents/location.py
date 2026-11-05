from __future__ import annotations

from uuid import UUID

from office365.runtime.client_value import ClientValue


class DocumentLocation(ClientValue):
    FolderId: int | None = None
    LibraryId: UUID | None = None
    SiteId: UUID | None = None
    WebId: UUID | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.ContentSolution.Models.Requests.DocumentLocation"
