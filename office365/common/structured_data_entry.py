from __future__ import annotations

from dataclasses import field

from office365.common.structured_data_entry_typed_value import StructuredDataEntryTypedValue
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class StructuredDataEntry(ClientValue):
    keyEntry: StructuredDataEntryTypedValue = field(default_factory=StructuredDataEntryTypedValue)
    valueEntry: StructuredDataEntryTypedValue = field(default_factory=StructuredDataEntryTypedValue)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.StructuredDataEntry"
