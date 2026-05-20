from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.identitygovernance.valuetype import ValueType
from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class Parameter(ClientValue):
    name: str | None = None
    values: StringCollection = field(default_factory=StringCollection)
    valueType: ValueType | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.identityGovernance.Parameter"
