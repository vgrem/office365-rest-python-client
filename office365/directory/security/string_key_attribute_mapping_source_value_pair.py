from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.security.attribute_mapping_source import AttributeMappingSource
from office365.runtime.client_value import ClientValue


@dataclass
class StringKeyAttributeMappingSourceValuePair(ClientValue):
    key: str | None = None
    value: AttributeMappingSource = field(default_factory=AttributeMappingSource)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.StringKeyAttributeMappingSourceValuePair"
