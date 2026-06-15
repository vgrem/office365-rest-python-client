from __future__ import annotations

from office365.runtime.client_value import ClientValue


class FieldInsertionItem(ClientValue):
    Content: str | None = None
    DataType: str | None = None
    Name: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Agreements.Models.FieldInsertionItem"
