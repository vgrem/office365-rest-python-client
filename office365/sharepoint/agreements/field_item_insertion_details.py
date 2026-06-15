from __future__ import annotations

from office365.runtime.client_value import ClientValue


class FieldItemInsertionDetails(ClientValue):
    ColumnId: str | None = None
    DataType: str | None = None
    FieldId: str | None = None
    Occurrences: int | None = None
    Text: str | None = None
    Title: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Agreements.Models.FieldItemInsertionDetails"
