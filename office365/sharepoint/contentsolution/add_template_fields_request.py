from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.contentsolution.field_input import FieldInput


class AddTemplateFieldsRequest(ClientValue):
    Fields: ClientValueCollection[FieldInput] = field(default_factory=lambda: ClientValueCollection(FieldInput))
    TemplateId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.ContentSolution.Models.Requests.AddTemplateFieldsRequest"
