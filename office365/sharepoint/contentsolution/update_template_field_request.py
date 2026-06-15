from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.contentsolution.field_update import FieldUpdate


class UpdateTemplateFieldRequest(ClientValue):
    FieldId: str | None = None
    TemplateId: str | None = None
    UpdatedField: FieldUpdate = field(default_factory=FieldUpdate)

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.ContentSolution.Models.Requests.UpdateTemplateFieldRequest"
