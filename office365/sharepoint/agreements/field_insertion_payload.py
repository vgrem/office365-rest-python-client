from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.agreements.field_insertion_item import FieldInsertionItem


class FieldInsertionPayload(ClientValue):
    Items: ClientValueCollection[FieldInsertionItem] = field(
        default_factory=lambda: ClientValueCollection(FieldInsertionItem)
    )
    TemplateUrl: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Agreements.Models.FieldInsertionPayload"
