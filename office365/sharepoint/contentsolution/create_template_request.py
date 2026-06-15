from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.contentsolution.field_input import FieldInput
from office365.sharepoint.contentsolution.file_reference import FileReference
from office365.sharepoint.documents.location import DocumentLocation


class CreateTemplateRequest(ClientValue):
    DocumentLocation: DocumentLocation = field(default_factory=DocumentLocation)
    Fields: ClientValueCollection[FieldInput] = field(default_factory=lambda: ClientValueCollection(FieldInput))
    FormId: str | None = None
    SourceFileReference: FileReference = field(default_factory=FileReference)
    TemplateName: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.ContentSolution.Models.Requests.CreateTemplateRequest"
