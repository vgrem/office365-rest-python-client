from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class PlaceholderV2(ClientValue):
    AdditionalFieldsData: Optional[str] = None
    ColumnId: Optional[str] = None
    ColumnInternalName: Optional[str] = None
    DataType: Optional[str] = None
    FieldLibraryMappedId: Optional[str] = None
    FieldLibraryMappedVersion: Optional[str] = None
    Id: Optional[str] = None
    IsColumnMappingActive: Optional[bool] = None
    IsMandatory: Optional[bool] = None
    Name: Optional[str] = None
    QuestionTitle: Optional[str] = None
    Source: Optional[str] = None
