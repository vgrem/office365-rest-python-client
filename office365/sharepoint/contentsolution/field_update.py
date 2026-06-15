from __future__ import annotations

from office365.runtime.client_value import ClientValue


class FieldUpdate(ClientValue):
    AdditionalFieldsData: str | None = None
    DataType: str | None = None
    Description: str | None = None
    DisplayName: str | None = None
    IsColumnMappingActive: bool | None = None
    IsMandatory: bool | None = None
    Name: str | None = None
    Source: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.ContentSolution.Models.Requests.FieldUpdate"
