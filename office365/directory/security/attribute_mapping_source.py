from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.security.string_key_attribute_mapping_source_value_pair import (
    StringKeyAttributeMappingSourceValuePair,
)
from office365.directory.synchronization.attributemappingsourcetype import AttributeMappingSourceType
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class AttributeMappingSource(ClientValue):
    expression: str | None = None
    name: str | None = None
    parameters: ClientValueCollection[StringKeyAttributeMappingSourceValuePair] = field(
        default_factory=lambda: ClientValueCollection(StringKeyAttributeMappingSourceValuePair)
    )
    type: AttributeMappingSourceType = AttributeMappingSourceType.Attribute

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AttributeMappingSource"
