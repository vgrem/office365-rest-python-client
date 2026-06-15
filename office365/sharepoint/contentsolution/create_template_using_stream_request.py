from __future__ import annotations

from dataclasses import field
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.contentsolution.field_input import FieldInput


class CreateTemplateUsingStreamRequest(ClientValue):
    DocumentFolderId: int | None = None
    DocumentLibraryId: UUID | None = None
    DocumentSiteId: UUID | None = None
    DocumentWebId: UUID | None = None
    Fields: ClientValueCollection[FieldInput] = field(default_factory=lambda: ClientValueCollection(FieldInput))
    FormId: str | None = None
    TemplateName: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.ContentSolution.Models.Requests.CreateTemplateUsingStreamRequest"
