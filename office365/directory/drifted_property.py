from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.json import Json
from office365.runtime.types.value import value


@value
class DriftedProperty(ClientValue):
    currentValue: Json = field(default_factory=Json)
    desiredValue: Json = field(default_factory=Json)
    propertyName: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DriftedProperty"
