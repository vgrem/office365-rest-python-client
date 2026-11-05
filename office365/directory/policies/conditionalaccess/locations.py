from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class ConditionalAccessLocations(ClientValue):
    excludeLocations: StringCollection = field(default_factory=StringCollection)
    includeLocations: StringCollection = field(default_factory=StringCollection)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ConditionalAccessLocations"
