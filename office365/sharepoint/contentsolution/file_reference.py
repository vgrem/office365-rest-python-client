from __future__ import annotations

from uuid import UUID

from office365.runtime.client_value import ClientValue


class FileReference(ClientValue):
    LibraryId: UUID | None = None
    SiteId: UUID | None = None
    UniqueId: UUID | None = None
    WebId: UUID | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.ContentSolution.Models.Requests.FileReference"
