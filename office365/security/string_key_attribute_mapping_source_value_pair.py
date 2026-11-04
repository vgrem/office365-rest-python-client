from __future__ import annotations

from typing import TYPE_CHECKING

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value

if TYPE_CHECKING:
    from office365.security.attribute_mapping_source import AttributeMappingSource


@value
class StringKeyAttributeMappingSourceValuePair(ClientValue):
    key: str | None = None
    value: AttributeMappingSource | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.StringKeyAttributeMappingSourceValuePair"
