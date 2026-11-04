from __future__ import annotations

from office365.directory.synchronization.attributetype import AttributeType
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class AttributeMappingParameterSchema(ClientValue):
    allowMultipleOccurrences: bool | None = None
    name: str | None = None
    required: bool | None = None
    type: AttributeType = AttributeType.String

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AttributeMappingParameterSchema"
