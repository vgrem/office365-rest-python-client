from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.fields.type import FieldType


@dataclass
class FieldCreationInformation(ClientValue):
    """Represents metadata about fields creation.

    Fields:
        Title: Display name of the field.
        FieldTypeKind: Type of the field.
        Description: Description of the field.
        LookupListId: Target list for the lookup field.
        LookupFieldName: Name of the field in the source list.
        LookupWebId: Identifier of the site containing the source list.
        Required: Whether the field requires a value.
        Formula: Formula for calculated fields.
        Choices: List of choices for Choice/MultiChoice fields.
        IsCompactName: Whether the field name is compact.
    """

    Title: str
    FieldTypeKind: FieldType
    Description: Optional[str] = None
    LookupListId: Optional[str] = None
    LookupFieldName: Optional[str] = None
    LookupWebId: Optional[str] = None
    Required: bool = False
    Formula: Optional[str] = None
    Choices: Optional[List[str]] = None
    IsCompactName: Optional[bool] = None

    def __post_init__(self) -> None:
        if self.FieldTypeKind in {FieldType.MultiChoice, FieldType.Choice} and self.Choices is not None:
            self.Choices = StringCollection(self.Choices)  # type: ignore[assignment]

    @property
    def entity_type_name(self) -> str:
        return "SP.FieldCreationInformation"
