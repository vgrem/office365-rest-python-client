from __future__ import annotations

from dataclasses import dataclass, field

from office365.common.structured_data_entry_typed_value import StructuredDataEntryTypedValue
from office365.runtime.client_value import ClientValue


@dataclass
class StructuredDataEntry(ClientValue):
    keyEntry: StructuredDataEntryTypedValue = field(default_factory=StructuredDataEntryTypedValue)
    valueEntry: StructuredDataEntryTypedValue = field(default_factory=StructuredDataEntryTypedValue)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.StructuredDataEntry"
