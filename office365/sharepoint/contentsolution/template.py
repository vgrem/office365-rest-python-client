from __future__ import annotations

from uuid import UUID

from office365.runtime.client_value import ClientValue


class Template(ClientValue):
    FullUrl: str | None = None
    Id: UUID | None = None
    IsEncrypted: bool | None = None
    ListItemId: int | None = None
    Name: str | None = None
    ServerRelativeUrl: str | None = None
    Status: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.ContentSolution.Models.Entities.Template"
