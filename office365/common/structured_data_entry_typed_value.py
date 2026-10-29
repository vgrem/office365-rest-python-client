from __future__ import annotations

from dataclasses import dataclass, field

from office365.common.structured_data_entry_value_type import StructuredDataEntryValueType
from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class StructuredDataEntryTypedValue(ClientValue):
    type: StructuredDataEntryValueType = StructuredDataEntryValueType.dateTime
    values: StringCollection = field(default_factory=StringCollection)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.StructuredDataEntryTypedValue"
